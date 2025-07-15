import os
import sys
from loguru import logger
from pyspark.sql import SparkSession
from schema.csv_schema import schema


logger.info("Initializing Spark session...")

# Spark session
spark = SparkSession.builder.appName("CSVStreamProcessor").getOrCreate()

data_input_path = os.path.join(os.path.dirname(__file__), "../data/input")
logger.info(f"Setting up stream read from dir: {data_input_path}")

# Read the CSV files from the input directory
if not os.path.exists(data_input_path):
    logger.error(f"Input directory: {data_input_path} does not exist. Please generate CSV files first.")
    sys.exit(1)
df = spark.readStream \
    .option("header", True) \
    .schema(schema) \
    .csv("data/input")

# Perform some transformations or aggregations
# Example: Count events by type
agg = df.groupBy("event").count()

# Start the streaming query to write the aggregated results to console
query = agg.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

# Log the input data to console for debugging
# query = df.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", False) \
#     .start()

logger.success("Stream processing started. Waiting for termination...")
query.awaitTermination() # ctrl + C to stop; stops violently, but works for demo purposes

