# PySpark Structured Streaming Configuration Options

This document provides a comprehensive guide to PySpark Structured Streaming and its various configuration options, organized by component.

## 🌊 What is PySpark Structured Streaming?

**PySpark Structured Streaming** is Apache Spark's scalable and fault-tolerant stream processing engine built on the Spark SQL engine. It treats live data streams as unbounded tables that are continuously appended to, allowing you to process streaming data using the same DataFrame/Dataset API used for batch processing.

### 🎯 **Key Concepts**

- **Unbounded Table Model**: Streaming data is conceptualized as an infinite table where new rows are continuously appended
- **Incremental Processing**: Only processes new data since the last trigger, making it efficient for large datasets
- **Fault Tolerance**: Automatic recovery from failures using checkpointing and write-ahead logs
- **Exactly-Once Semantics**: Guarantees that each record is processed exactly once, even in case of failures
- **Unified API**: Same DataFrame/SQL API for both batch and streaming, enabling code reuse

### 🔄 **How It Works**

1. **Input Sources**: Read data from various sources (files, Kafka, sockets, etc.)
2. **Processing**: Apply transformations using DataFrame operations (select, filter, groupBy, etc.)
3. **Output Sinks**: Write results to various destinations (console, files, databases, etc.)
4. **Triggers**: Control when to execute the streaming query (continuous, interval-based, or one-time)

### 🏗️ **Core Components**

| Component           | Description                          | Examples                                     |
| ------------------- | ------------------------------------ | -------------------------------------------- |
| **Sources**         | Where streaming data comes from      | Files, Kafka, TCP sockets, Rate source       |
| **Transformations** | Operations applied to streaming data | select(), filter(), groupBy(), join()        |
| **Sinks**           | Where processed data is written      | Console, files, Kafka, memory, foreach       |
| **Triggers**        | When to process new data             | Default, fixed interval, once, available now |
| **Checkpointing**   | Fault tolerance mechanism            | Saves query state for recovery               |

### 📊 **Processing Model**

```
Input Stream → DataFrame → Transformations → Output Stream
     ↓              ↓             ↓             ↓
  [Files]    [Unbounded Table] [SQL/DF Ops]  [Results]
```

### ✨ **Benefits**

- **Scalability**: Automatically scales across multiple machines
- **Fault Tolerance**: Recovers from node failures without data loss
- **Low Latency**: Sub-second processing capabilities
- **Exactly-Once Processing**: Strong consistency guarantees
- **Rich Operations**: Full DataFrame/SQL API support
- **Integration**: Works with existing Spark ecosystem (MLlib, GraphX, etc.)

### 🎯 **Common Use Cases**

- **Real-time Analytics**: Live dashboards, metrics, KPIs
- **ETL Pipelines**: Continuous data transformation and loading
- **Event Processing**: IoT data, clickstreams, sensor data
- **Fraud Detection**: Real-time anomaly detection
- **Monitoring**: Log analysis, alerting systems
- **Data Lake Ingestion**: Continuous data ingestion to storage systems

---

## 📋 Table of Contents

- [What is PySpark Structured Streaming?](#what-is-pyspark-structured-streaming)
- [Quick Start Guide](#quick-start-guide)
- [Reading Data (Source Options)](#reading-data-source-options)
- [Schema Configuration](#schema-configuration)
- [Data Formats](#data-formats)
- [Aggregation Operations](#aggregation-operations)
- [Output Modes](#output-modes)
- [Output Formats (Sinks)](#output-formats-sinks)
- [Trigger Modes](#trigger-modes)
- [Common Options](#common-options)
- [Performance Tuning](#performance-tuning)
- [Best Practices](#best-practices)

---

## 🚀 Quick Start Guide

Here's a minimal example to get you started:

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, IntegerType

# Create Spark session
spark = SparkSession.builder.appName("StreamingExample").getOrCreate()

# Define schema (recommended for production)
schema = StructType() \
    .add("timestamp", StringType()) \
    .add("user_id", IntegerType()) \
    .add("event", StringType())

# Read streaming data
df = spark.readStream \
    .option("header", True) \
    .schema(schema) \
    .csv("path/to/input/directory")

# Process data (example: count events by type)
event_counts = df.groupBy("event").count()

# Write results
query = event_counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("checkpointLocation", "path/to/checkpoint") \
    .start()

# Wait for termination
query.awaitTermination()
```

---

## 💡 Best Practices

1. **Always specify schema** for production workloads - improves performance and prevents errors
2. **Use checkpointing** for fault tolerance - essential for production deployments
3. **Monitor query metrics** for performance - track input/processing rates and batch durations
4. **Choose appropriate output mode** based on use case - append for raw data, complete/update for aggregations
5. **Use watermarking** for event time processing - handles late-arriving data properly
6. **Partition output** for better performance - improves query performance and file organization
7. **Handle late data** with watermarks - prevents unbounded state growth
8. **Use appropriate trigger mode** for latency requirements - balance between latency and throughput
9. **Test with small datasets** first - validate logic before processing large streams
10. **Design for idempotency** - ensure operations can be safely retried

---

## 📖 Reading Data (Source Options)

### File-based Sources (CSV, JSON, Parquet)

| Option                | Description                      | Default Value | Example                                | Use Case                    |
| --------------------- | -------------------------------- | ------------- | -------------------------------------- | --------------------------- |
| `header`              | Whether files have header row    | `False`       | `.option("header", True)`              | CSV files with column names |
| `sep` / `delimiter`   | Field separator                  | `","`         | `.option("sep", ";")`                  | Custom delimited files      |
| `inferSchema`         | Auto-detect column types         | `False`       | `.option("inferSchema", True)`         | When schema is unknown      |
| `multiline`           | Support multi-line records       | `False`       | `.option("multiline", True)`           | JSON with nested objects    |
| `maxFilesPerTrigger`  | Max files per batch              | No limit      | `.option("maxFilesPerTrigger", 10)`    | Control batch size          |
| `latestFirst`         | Process newest files first       | `False`       | `.option("latestFirst", True)`         | Priority to recent data     |
| `fileNameOnly`        | Use only filename for processing | `False`       | `.option("fileNameOnly", True)`        | Ignore path changes         |
| `pathGlobFilter`      | Filter files by pattern          | `"*"`         | `.option("pathGlobFilter", "*.csv")`   | Specific file types         |
| `recursiveFileLookup` | Search subdirectories            | `False`       | `.option("recursiveFileLookup", True)` | Nested directory structure  |

```python
# Example: Advanced CSV reading
df = spark.readStream \
    .option("header", True) \
    .option("sep", ",") \
    .option("maxFilesPerTrigger", 5) \
    .option("latestFirst", True) \
    .schema(schema) \
    .csv("data/input")
```

### Socket Sources

| Option             | Description          | Default Value | Example                             | Use Case              |
| ------------------ | -------------------- | ------------- | ----------------------------------- | --------------------- |
| `host`             | Server hostname      | `"localhost"` | `.option("host", "localhost")`      | WebSocket connection  |
| `port`             | Server port          | Required      | `.option("port", 9999)`             | Network communication |
| `includeTimestamp` | Add timestamp column | `False`       | `.option("includeTimestamp", True)` | Event time tracking   |

```python
# Example: Socket with timestamp
socketDF = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .option("includeTimestamp", True) \
    .load()
```

### Kafka Sources

| Option                    | Description            | Default Value | Example                                           | Use Case           |
| ------------------------- | ---------------------- | ------------- | ------------------------------------------------- | ------------------ |
| `kafka.bootstrap.servers` | Kafka brokers          | Required      | `.option("kafka.bootstrap.servers", "host:port")` | Kafka connection   |
| `subscribe`               | Topic subscription     | Required\*    | `.option("subscribe", "topic1,topic2")`           | Multiple topics    |
| `subscribePattern`        | Topic pattern          | Required\*    | `.option("subscribePattern", "topic.*")`          | Dynamic topics     |
| `startingOffsets`         | Where to start reading | `"latest"`    | `.option("startingOffsets", "earliest")`          | Start position     |
| `endingOffsets`           | Where to stop (batch)  | `"latest"`    | `.option("endingOffsets", "latest")`              | End position       |
| `maxOffsetsPerTrigger`    | Rate limiting          | No limit      | `.option("maxOffsetsPerTrigger", 10000)`          | Control throughput |

\*Either `subscribe` or `subscribePattern` is required, not both.

```python
# Example: Kafka streaming
kafkaDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "events") \
    .option("startingOffsets", "earliest") \
    .load()
```

---

## 🗂️ Schema Configuration

### Schema Definition Methods

| Method               | Description                | Default Behavior       | When to Use              | Example                                  |
| -------------------- | -------------------------- | ---------------------- | ------------------------ | ---------------------------------------- |
| **Explicit Schema**  | Define exact structure     | N/A                    | Production, type safety  | `StructType().add("name", StringType())` |
| **Schema Inference** | Auto-detect from data      | Disabled for streaming | Development, exploration | `.option("inferSchema", True)`           |
| **DDL String**       | SQL-like schema definition | N/A                    | Simple structures        | `"name STRING, age INT"`                 |

```python
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType

# Method 1: Explicit Schema (Recommended)
schema = StructType() \
    .add("timestamp", TimestampType()) \
    .add("user_id", IntegerType()) \
    .add("event", StringType()) \
    .add("amount", "double")

# Method 2: DDL String
schema_ddl = "timestamp TIMESTAMP, user_id INT, event STRING, amount DOUBLE"

# Method 3: Schema from existing DataFrame
schema = existing_df.schema
```

### Schema Evolution

| Approach            | Description                         | Default Behavior | Use Case                 |
| ------------------- | ----------------------------------- | ---------------- | ------------------------ |
| **mergeSchema**     | Combine schemas from multiple files | `False`          | Schema changes over time |
| **Schema Registry** | External schema management          | Not used         | Enterprise environments  |
| **Union Types**     | Handle multiple schemas             | Not supported    | Heterogeneous data       |

---

## 📁 Data Formats

### Input Formats

| Format      | Method              | Schema Required | Default Schema Behavior  | Use Case                     |
| ----------- | ------------------- | --------------- | ------------------------ | ---------------------------- |
| **CSV**     | `.csv(path)`        | Recommended     | All columns as strings   | Structured tabular data      |
| **JSON**    | `.json(path)`       | Optional        | Inferred from first file | Semi-structured data         |
| **Parquet** | `.parquet(path)`    | No              | Read from file metadata  | Columnar, compressed data    |
| **Text**    | `.text(path)`       | No              | Single "value" column    | Log files, unstructured data |
| **Socket**  | `.format("socket")` | No              | Single "value" column    | Real-time text streams       |
| **Kafka**   | `.format("kafka")`  | No              | Predefined Kafka schema  | Message queues               |
| **Delta**   | `.format("delta")`  | No              | Read from Delta metadata | ACID transactions            |

```python
# CSV with options
df = spark.readStream.option("header", True).schema(schema).csv("path")

# JSON with schema inference
df = spark.readStream.option("multiline", True).json("path")

# Parquet (schema included)
df = spark.readStream.parquet("path")

# Text files
df = spark.readStream.text("path")

# Delta Lake
df = spark.readStream.format("delta").load("path")
```

---

## 🔢 Aggregation Operations

### Basic Aggregations

| Function           | Description               | Default Behavior | Output Mode      | Example                                         |
| ------------------ | ------------------------- | ---------------- | ---------------- | ----------------------------------------------- |
| **count()**        | Count rows                | Count all rows   | Complete, Update | `df.groupBy("category").count()`                |
| **sum()**          | Sum values                | Sum non-null     | Complete, Update | `df.groupBy("category").sum("amount")`          |
| **avg()**          | Average values            | Mean of non-null | Complete, Update | `df.groupBy("category").avg("price")`           |
| **min()**          | Minimum value             | Minimum non-null | Complete, Update | `df.groupBy("category").min("timestamp")`       |
| **max()**          | Maximum value             | Maximum non-null | Complete, Update | `df.groupBy("category").max("timestamp")`       |
| **collect_list()** | Collect values into array | All values       | Complete         | `df.groupBy("user").agg(collect_list("event"))` |

### Advanced Aggregations

| Function                    | Description              | Default Behavior         | Use Case             |
| --------------------------- | ------------------------ | ------------------------ | -------------------- |
| **approx_count_distinct()** | Approximate unique count | 5% relative error        | Large datasets       |
| **percentile_approx()**     | Approximate percentiles  | 10000 accuracy parameter | Statistical analysis |
| **stddev()**                | Standard deviation       | Population std dev       | Data quality metrics |
| **variance()**              | Variance calculation     | Population variance      | Statistical analysis |

```python
from pyspark.sql.functions import *

# Basic aggregations
basic_agg = df.groupBy("event").count()

# Multiple aggregations
multi_agg = df.groupBy("user_id").agg(
    count("*").alias("event_count"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("avg_amount"),
    max("timestamp").alias("last_event")
)

# Window functions
from pyspark.sql.window import Window

window = Window.partitionBy("user_id").orderBy("timestamp")
windowed_df = df.withColumn("running_total", sum("amount").over(window))
```

### Time-based Aggregations

| Function             | Description           | Default Behavior    | Example                                          |
| -------------------- | --------------------- | ------------------- | ------------------------------------------------ |
| **window()**         | Time windows          | No overlap          | `window(col("timestamp"), "10 minutes")`         |
| **session_window()** | Session-based windows | No gap tolerance    | `session_window(col("timestamp"), "30 minutes")` |
| **tumbling window**  | Fixed-size windows    | No overlap          | `window(col("time"), "1 hour")`                  |
| **sliding window**   | Overlapping windows   | Custom slide period | `window(col("time"), "1 hour", "30 minutes")`    |

```python
# Tumbling window (non-overlapping)
tumbling = df.groupBy(
    window(col("timestamp"), "10 minutes")
).count()

# Sliding window (overlapping)
sliding = df.groupBy(
    window(col("timestamp"), "10 minutes", "5 minutes")
).count()

# Session window
session = df.groupBy(
    session_window(col("timestamp"), "30 minutes")
).count()
```

---

## 📤 Output Modes

| Mode         | Description         | Default Usage                        | When to Use                            | Supported Operations      |
| ------------ | ------------------- | ------------------------------------ | -------------------------------------- | ------------------------- |
| **append**   | Only new rows       | Default for non-aggregated queries   | Non-aggregated queries, immutable data | Selections, filters, maps |
| **complete** | All rows every time | Required for most aggregations       | Small result sets, aggregations        | All aggregations          |
| **update**   | Only changed rows   | Available for key-based aggregations | Large result sets with updates         | Aggregations with keys    |

```python
# Append mode - for raw data
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Complete mode - for aggregations (shows all aggregated results every batch)
query = df.groupBy("event").count().writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

# Update mode - for key-based aggregations (only shows changed aggregation keys)
# Example: User activity count per user
# Batch 1: user1=5, user2=3 (first time seeing these users)
# Batch 2: user1=8, user3=2 (only user1 count changed, user3 is new)
# Output will only show: user1=8, user3=2 (not user2=3 since unchanged)
user_activity = df.groupBy("user_id").count().writeStream \
    .outputMode("update") \
    .format("console") \
    .start()
```

---

## 🖥️ Output Formats (Sinks)

### Console Sink

**Purpose**: Displays streaming results in the terminal for development and debugging.

| Option     | Description               | Default Value | Example                      |
| ---------- | ------------------------- | ------------- | ---------------------------- |
| `truncate` | Truncate long values      | `True`        | `.option("truncate", False)` |
| `numRows`  | Number of rows to display | `20`          | `.option("numRows", 50)`     |

```python
query = df.writeStream \
    .format("console") \
    .option("truncate", False) \
    .option("numRows", 100) \
    .start()
```

### File Sinks

**Purpose**: Persist streaming data to distributed file systems for long-term storage and analytics.

| Format      | Description       | Default Options           | Available Options                | Use Case              |
| ----------- | ----------------- | ------------------------- | -------------------------------- | --------------------- |
| **Parquet** | Columnar format   | `compression=snappy`      | `compression`, `partitionBy`     | Analytics, data lakes |
| **JSON**    | JSON Lines format | Standard timestamp format | `timestampFormat`, `dateFormat`  | Log processing        |
| **CSV**     | Comma-separated   | `header=false`, `sep=","` | `header`, `sep`, `quote`         | Data export           |
| **Delta**   | ACID transactions | `mergeSchema=false`       | `mergeSchema`, `overwriteSchema` | Data warehousing      |

> see "Common Options/Checkpointing" below to understand .option("checkpointLocation",...)

```python
# Parquet output with compression and partitioning
query = df.writeStream \
    .format("parquet") \
    .option("path", "output/parquet") \
    .option("checkpointLocation", "checkpoints/parquet") \
    .option("compression", "gzip") \
    .partitionBy("date") \
    .start()

# JSON output with custom timestamp format
query = df.writeStream \
    .format("json") \
    .option("path", "output/json") \
    .option("checkpointLocation", "checkpoints/json") \
    .option("timestampFormat", "yyyy-MM-dd HH:mm:ss") \
    .option("dateFormat", "yyyy-MM-dd") \
    .start()

# CSV output with headers and custom separator
query = df.writeStream \
    .format("csv") \
    .option("path", "output/csv") \
    .option("checkpointLocation", "checkpoints/csv") \
    .option("header", "true") \
    .option("sep", "|") \
    .option("quote", '"') \
    .start()

# Delta output with schema evolution
query = df.writeStream \
    .format("delta") \
    .option("path", "output/delta") \
    .option("checkpointLocation", "checkpoints/delta") \
    .option("mergeSchema", "true") \
    .start()
```

### Memory Sink

**Purpose**: Stores streaming results in memory as a temporary table for interactive querying and testing.

```python
# Memory sink for testing - creates an in-memory table
query = df.writeStream \
    .format("memory") \
    .queryName("my_table") \
    .start()

# Query the in-memory table (can be done in another cell/session)
spark.sql("SELECT * FROM my_table").show()
spark.sql("SELECT event, count(*) FROM my_table GROUP BY event").show()
```

### Custom Sinks

**Purpose**: Implement custom logic for processing each row or batch of streaming data.

```python
# Foreach sink - process each row individually
def process_row(row):
    # Custom processing logic (e.g., send to external API, database insert)
    print(f"Processing: {row}")

query = df.writeStream \
    .foreach(process_row) \
    .start()

# ForeachBatch sink - process entire batches
def process_batch(batch_df, batch_id):
    # Process entire batch (e.g., bulk database operations, complex transformations)
    print(f"Processing batch {batch_id} with {batch_df.count()} rows")
    batch_df.write.mode("append").saveAsTable("processed_data")

query = df.writeStream \
    .foreachBatch(process_batch) \
    .start()
```

---

## ⏰ Trigger Modes

| Mode                      | Description                 | Default Behavior         | When to Use            | Example                                |
| ------------------------- | --------------------------- | ------------------------ | ---------------------- | -------------------------------------- |
| **Default (Micro-batch)** | Process as soon as possible | Used when no trigger set | Low latency            | No trigger specified                   |
| **Fixed Interval**        | Process every X time        | N/A                      | Batch-like processing  | `trigger(processingTime='30 seconds')` |
| **One-time**              | Process once and stop       | N/A                      | Batch jobs             | `trigger(once=True)`                   |
| **Available Now**         | Process all available data  | N/A                      | Catch-up processing    | `trigger(availableNow=True)`           |
| **Continuous**            | Ultra-low latency           | N/A (experimental)       | Real-time requirements | `trigger(continuous='1 second')`       |

```python
# Default: Process immediately
query = df.writeStream.format("console").start()

# Fixed interval
query = df.writeStream \
    .trigger(processingTime='30 seconds') \
    .format("console").start()

# One-time processing
query = df.writeStream \
    .trigger(once=True) \
    .format("console").start()

# Available now
query = df.writeStream \
    .trigger(availableNow=True) \
    .format("console").start()

# Continuous processing (experimental)
query = df.writeStream \
    .trigger(continuous='1 second') \
    .format("console").start()
```

---

## ⚙️ Common Options

### Checkpointing

**Purpose**: Provides fault tolerance by saving streaming query state to persistent storage. Enables recovery from failures and exactly-once processing guarantees.

| Option               | Description               | Default Behavior        | Required | Example                                               |
| -------------------- | ------------------------- | ----------------------- | -------- | ----------------------------------------------------- |
| `checkpointLocation` | Fault tolerance directory | Auto-generated temp dir | No\*     | `.option("checkpointLocation", "path/to/checkpoint")` |

\*Required for production use with file sinks and fault tolerance.

```python
# Recommended for production - enables fault tolerance and state recovery
query = df.writeStream \
    .option("checkpointLocation", "path/to/checkpoint") \  # Saves query state here
    .format("parquet") \
    .start()

# Default behavior (not recommended for production)
query = df.writeStream \
    .format("console") \  # No checkpoint needed for console output
    .start()  # Uses temporary checkpoint location that gets deleted
```

### Query Management

**Purpose**: Control the lifecycle of streaming queries - start, monitor, and stop streaming operations.

| Method/Property             | Description                           | Default Behavior                                | Example                              |
| --------------------------- | ------------------------------------- | ----------------------------------------------- | ------------------------------------ |
| `start()`                   | Start the streaming query             | Returns StreamingQuery                          | `query = df.writeStream.start()`     |
| `query.id`                  | Unique query identifier               | Auto-generated UUID                             | `print(f"Query ID: {query.id}")`     |
| `query.isActive`            | Check if query is running             | `True` after start                              | `print(f"Active: {query.isActive}")` |
| `query.status`              | Current query status                  | Status object                                   | `print(f"Status: {query.status}")`   |
| `stop()`                    | Stop the streaming query              | Graceful shutdown                               | `query.stop()`                       |
| `awaitTermination()`        | Wait indefinitely for query to finish | Blocks until query stops (manual stop or error) | `query.awaitTermination()`           |
| `awaitTermination(timeout)` | Wait with timeout for query to finish | Blocks for specified seconds, then continues    | `query.awaitTermination(60)`         |

```python
# Start query
query = df.writeStream.format("console").start()

# Check status
print(f"Query ID: {query.id}")
print(f"Is Active: {query.isActive}")
print(f"Status: {query.status}")

# Stop query
query.stop()

# Wait for termination (blocks forever until manual stop or error)
query.awaitTermination()

# Wait with timeout (blocks for 60 seconds, then continues execution)
query.awaitTermination(timeout=60)  # Returns True if stopped, False if timeout
```

### Error Handling

**Purpose**: Monitor streaming query progress and detect processing issues like slow batches or failed operations.

```python
# Progress reporting - monitor streaming query performance
def print_progress(progress):
    print(f"Batch: {progress.batchId}, Records: {progress.inputRowsPerSecond}")

query = df.writeStream \
    .format("console") \
    .start()

# Monitor progress - get metrics from recent batches
for progress in query.recentProgress:
    print(progress)
```

---

## 🚀 Performance Tuning

### Optimization Options

**Purpose**: Control resource usage and processing rates to optimize streaming performance for your workload.

| Parameter                            | Description           | Default Value | Example                                                        |
| ------------------------------------ | --------------------- | ------------- | -------------------------------------------------------------- |
| `maxFilesPerTrigger`                 | Limit files per batch | No limit      | `.option("maxFilesPerTrigger", 10)`                            |
| `maxOffsetsPerTrigger`               | Limit Kafka offsets   | No limit      | `.option("maxOffsetsPerTrigger", 10000)`                       |
| `spark.sql.streaming.metricsEnabled` | Enable metrics        | `False`       | `spark.conf.set("spark.sql.streaming.metricsEnabled", "true")` |

### Memory Management

**Purpose**: Configure Spark settings to optimize memory usage and query execution for streaming workloads.

| Configuration                                   | Description                    | Default Value | Example Value      |
| ----------------------------------------------- | ------------------------------ | ------------- | ------------------ |
| `spark.sql.adaptive.enabled`                    | Enable adaptive query planning | `True`        | `"true"`           |
| `spark.sql.adaptive.coalescePartitions.enabled` | Auto-coalesce partitions       | `True`        | `"true"`           |
| `spark.serializer`                              | Serialization method           | Java          | `"KryoSerializer"` |

```python
# Configure Spark for streaming with default improvements
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
```

### Monitoring

**Purpose**: Track streaming query performance metrics to identify bottlenecks and optimize processing rates.

```python
# Stream metrics - analyze query performance
query = df.writeStream.format("console").start()

# Get recent progress - examine processing statistics
progress = query.recentProgress
for p in progress:
    print(f"Input rate: {p['inputRowsPerSecond']}")        # Data ingestion rate
    print(f"Processing rate: {p['processingRowsPerSecond']}")  # Data processing rate
    print(f"Batch duration: {p['durationMs']}")           # Time to process each batch
```
