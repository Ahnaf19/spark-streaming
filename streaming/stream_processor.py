import sys
import argparse
from loguru import logger
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col
from pyspark.sql.functions import explode

from schema.csv_schema import schema
from utils.utils import setup_data_input_path


INPUT_PATH = "data/input"
PROCESSING_TIME = '5 seconds'
HOST = "localhost"
PORT = 9999

def create_spark_session(app_name: str) -> SparkSession:
    """Create and return a Spark session."""
    logger.info(f"Initializing Spark session: {app_name}")
    return SparkSession.builder.appName(app_name).getOrCreate()

def run_csv_aggregation(spark: SparkSession, processing_time: str = PROCESSING_TIME):
    """Run CSV streaming with aggregation (count events by type).
    
    Workflow: Monitors data/input directory → Reads new CSV files → Groups events by type 
    → Counts occurrences → Displays aggregated results in real-time.
    """
    logger.info("Starting CSV streaming with aggregation...")
    
    setup_data_input_path(INPUT_PATH)
    
    # Read CSV stream
    df = spark.readStream \
        .option("header", True) \
        .schema(schema) \
        .csv(INPUT_PATH)
    
    # Perform aggregation: Count events by type
    # explore with other aggregations like sum, avg, etc.
    logger.info("Performing aggregation: Counting events by type...")
    agg = df.groupBy("event").count()
    
    # Start streaming query with aggregation
    query = agg.writeStream \
        .outputMode("complete") \
        .format("console") \
        .option("truncate", False) \
        .trigger(processingTime=processing_time) \
        .start()
    
    logger.success("CSV aggregation stream started. Press Ctrl+C to stop...")
    return query

def run_csv_log_only(spark: SparkSession, processing_time: str = PROCESSING_TIME):
    """Run CSV streaming with log output only (no aggregation).
    
    Workflow: Monitors data/input directory → Reads new CSV files → Displays raw event data without any processing 
    → Shows individual records in real-time.
    """
    logger.info("Starting CSV streaming with log output only...")

    setup_data_input_path(INPUT_PATH)

    # Read CSV stream
    df = spark.readStream \
        .option("header", True) \
        .schema(schema) \
        .csv(INPUT_PATH)
    
    # Start streaming query with raw data output
    query = df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", False) \
        .trigger(processingTime=processing_time) \
        .start()
    
    logger.success("CSV log-only stream started. Press Ctrl+C to stop...")
    return query


def run_websocket_stream(spark: SparkSession, host: str = HOST, port: int = PORT, processing_time: str = PROCESSING_TIME):
    """Run WebSocket streaming for real-time text processing.
    
    Workflow: Connects to socket server (localhost:9999) → Receives text lines from socket connection → Splits text into words 
    → Counts word occurrences → Displays word count results in real-time.
    """
    logger.info(f"Starting WebSocket streaming from {host}:{port}...")
    logger.warning("Make sure to start a socket server first! Example:")
    logger.warning(f"  nc -lk {port}  # On macOS/Linux")
    logger.warning("Then type text messages in the terminal to send to the stream.")
    
    try:
        # Read text from socket
        socketDF = spark \
            .readStream \
            .format("socket") \
            .option("host", host) \
            .option("port", port) \
            .load()
        # socketDF contains a single column "value" with the text data
        
        logger.info(f"Socket stream is streaming: {socketDF.isStreaming}")
        logger.info("Socket stream schema:")
        socketDF.printSchema()
        
        # Split lines into words and count them
        words = socketDF.select(
            split(col("value"), " ").alias("words")
        ).select("words").where("words is not null")
        
        # Flatten the array of words and count each word
        word_counts = words.select(
            explode(col("words")).alias("word")  # Explodes array to individual rows
        ).groupBy("word").count()
        
        # Start streaming query
        query = word_counts.writeStream \
            .outputMode("complete") \
            .format("console") \
            .option("truncate", False) \
            .trigger(processingTime=processing_time) \
            .start()
        
        logger.success("WebSocket stream started. Press Ctrl+C to stop...")
        return query
        
    except Exception as e:
        logger.error(f"Failed to connect to socket {host}:{port}. Error: {e}")
        logger.error("Make sure the socket server is running!")
        sys.exit(1)


def main():
    """Main function with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="PySpark Structured Streaming Processor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python stream_processor.py --mode csv-agg          # CSV with aggregation
  python stream_processor.py --mode csv-log          # CSV log only
  python stream_processor.py --mode websocket        # WebSocket stream
  python stream_processor.py --mode websocket --host localhost --port 8888
        """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["csv-agg", "csv-log", "websocket"],
        default="csv-agg",
        help="Streaming mode: csv-agg (CSV with aggregation), csv-log (CSV log only), websocket (WebSocket stream)"
    )
    
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for WebSocket connection (default: localhost)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=9999,
        help="Port for WebSocket connection (default: 9999)"
    )
    
    args = parser.parse_args()
    
    # Create Spark session based on mode
    app_name = f"StreamProcessor-{args.mode}"
    spark = create_spark_session(app_name)
    
    try:
        # Run the appropriate streaming mode
        if args.mode == "csv-agg":
            query = run_csv_aggregation(spark)
        elif args.mode == "csv-log":
            query = run_csv_log_only(spark)
        elif args.mode == "websocket":
            query = run_websocket_stream(spark, args.host, args.port)
        
        # Wait for termination
        query.awaitTermination()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal. Stopping stream...")
    except Exception as e:
        logger.error(f"Stream processing failed: {e}")
    finally:
        logger.info("Stopping Spark session...")
        spark.stop()


if __name__ == "__main__":
    main()

