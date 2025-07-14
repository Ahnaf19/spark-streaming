from loguru import logger
from pyspark.sql import SparkSession
from schema.csv_schema import schema

logger.info("Initializing Spark session...")

spark = SparkSession.builder.appName("CSVStreamProcessor").getOrCreate()

logger.info("Setting up stream read from dir: data/input")

# Read the CSV files from the input directory
# Ensure the directory exists and contains CSV files
df = spark.readStream \
    .option("header", True) \
    .schema(schema) \
    .csv("data/input")

# Perform some transformations or aggregations
# Example: Count events by type
logger.info("Performing aggregations on the stream...")
agg = df.groupBy("event").count()

# Start the streaming query to write the aggregated results to console
logger.info("Starting streaming query...")
query = agg.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

logger.success("Stream processing started. Waiting for termination...")
query.awaitTermination()
