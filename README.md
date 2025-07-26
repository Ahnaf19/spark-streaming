# PySpark Structured Streaming

This project demonstrates real-time data processing using PySpark Structured Streaming. It simulates a continuous data stream by generating CSV files and processes them in real-time to perform aggregations and transformations.

> [!NOTE]
> Developed on `python 3.5. **Production Similarity**: Similar to real-time chat, log, or sensor data streams

## Sample Output

### CSV Aggregation Mode (`--mode csv-agg`)

When running the stream processor with aggregation, you'll see output like:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Spark](https://img.shields.io/badge/spark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white) ![Loguru](https://img.shields.io/badge/loguru-FF9C00?style=for-the-badge&logo=python&logoColor=white) ![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

## 📋 Table of Contents

- [What is PySpark Structured Streaming?](#what-is-pyspark-structured-streaming)
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)`
- [Running the Project](#running-the-project)
- [What's Happening Step by Step](#whats-happening-step-by-step)
- [Sample Output](#sample-output)
- [Configuration Options](#configuration-options)
- [Troubleshooting](#troubleshooting)
- [Learning Objectives](#learning-objectives)

## What is PySpark Structured Streaming?

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

## Project Overview

This project simulates a real-world streaming scenario where:

1. **Data Generator**: Continuously generates CSV files with user event data (login, logout, purchase, view)
2. **Stream Processor**: Uses PySpark Structured Streaming to monitor the input directory and process new files in real-time
3. **Real-time Analytics**: Performs aggregations (counting events by type) and displays results to the console

### 🆕 **New Features**

- **Multiple Streaming Modes**: CSV aggregation, CSV log-only, and WebSocket streaming
- **CLI Interface**: Easy mode switching with command-line arguments
- **Comprehensive Documentation**: Detailed configuration options guide
- **Production-Ready**: Proper error handling, checkpointing, and monitoring

## Project Structure

```
spark-streaming/
├── README.md                           # Project documentation
├── LICENSE                             # MIT license
├── requirements.txt                    # Python dependencies
├── data/
│   └── input/                          # Directory where CSV files are generated
│       ├── event_batch_0.csv           # Sample event data files
│       ├── event_batch_1.csv
│       └── ...
├── generator/
│   └── csv_writer.py                   # Script to generate CSV files
├── schema/
│   ├── __init__.py
│   └── csv_schema.py                   # PySpark schema definition
└── streaming/
    ├── README.md                       # 📚 Comprehensive configuration guide
    ├── stream_processor.py             # Main streaming application
    └── utils/
        └── utils.py                    # Utility functions for path handling
```

> [!TIP]
> 📚 **For detailed configuration options**, see [`streaming/README.md`](streaming/README.md) - a comprehensive guide covering all PySpark Structured Streaming configuration options with examples and best practices.

## Prerequisites

- **Python 3.8 or newer** (Python 3.10+ recommended for better type hints support)
- **Java 8 or 11** (required for PySpark)
- **Apache Spark** (will be installed via PySpark)

### Check Java Installation

```bash
java -version
```

If Java is not installed on macOS, install it using:

```bash
brew install openjdk@11
```

## Setup Instructions

### 1. Clone or Download the Repository

```bash
# If using git
git clone <repository-url>

# Or download and extract the project files
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Test PySpark installation
python -c "from pyspark.sql import SparkSession; print('PySpark installed successfully!')"
```

## Running the Project

> First export repo root as PYTHONPATH

```bash
# linux or macOS
export PYTHONPATH=.

# windows
$env:PYTHONPATH = "." # powershell
set PYTHONPATH=. # cmd
```

The stream processor now supports three different modes via CLI options:

### Mode 1: CSV with Aggregation (Default)

Processes CSV files and shows event count aggregations:

```bash
python streaming/stream_processor.py --mode csv-agg
# OR simply:
python streaming/stream_processor.py
```

### Mode 2: CSV Log Only

Processes CSV files and displays raw data without aggregation:

```bash
python streaming/stream_processor.py --mode csv-log
```

### Mode 3: WebSocket Streaming

Reads text data from a WebSocket connection and performs word count:

```bash
# First, start a socket server in another terminal:
nc -lk 9999  # On macOS/Linux (netcat)

# Then start the stream processor:
python streaming/stream_processor.py --mode websocket

# Or with custom host/port:
python streaming/stream_processor.py --mode websocket --host localhost --port 8888
```

### Data Generation for CSV Modes

For CSV modes, generate data using:

```bash
python generator/csv_writer.py
```

### Complete Example Workflows

#### CSV Aggregation Workflow:

1. **Terminal 1 - Start Stream Processor:**

```bash
python streaming/stream_processor.py --mode csv-agg
```

2. **Terminal 2 - Generate Data:**

```bash
python generator/csv_writer.py
```

#### WebSocket Workflow:

1. **Terminal 1 - Start Socket Server:**

```bash
nc -lk 9999
```

2. **Terminal 2 - Start Stream Processor:**

```bash
python streaming/stream_processor.py --mode websocket
```

3. **Terminal 1 - Type messages** to send to the stream (press Enter after each message)

### CLI Options Reference

```bash
python streaming/stream_processor.py --help
```

Available options:

- `--mode`: Choose streaming mode (`csv-agg`, `csv-log`, `websocket`)
- `--host`: WebSocket host (default: localhost)
- `--port`: WebSocket port (default: 9999)

> 💡 [!TIP]: For instant processing without delays, remove the trigger or use different trigger modes. See the [Configuration Options](#configuration-options) section below for details.

### Stopping the Application

- Press `Ctrl+C` in the stream processor terminal to stop the streaming query
- The data generator will stop automatically after creating 10 files

## What's Happening Step by Step

### CSV Streaming Modes (csv-agg & csv-log)

#### Phase 1: Data Generation

1. **CSV Writer Initialization**: The `csv_writer.py` script creates the `data/input` directory
2. **File Generation**: Generates 10 CSV files (`event_batch_0.csv` to `event_batch_9.csv`) with a 3-second delay between each
3. **Data Structure**: Each file contains 10 rows of simulated user events with:
   - `timestamp`: Current datetime in ISO format
   - `user_id`: Random integer between 1-5
   - `event`: Random choice from ["login", "logout", "purchase", "view"]

#### Phase 2: Schema Definition

1. **Schema Setup**: The `csv_schema.py` defines the structure of incoming data
2. **Type Safety**: Ensures PySpark knows the data types (timestamp as string, user_id as integer, event as string)

#### Phase 3: Stream Processing

1. **Spark Session**: Creates a Spark session with mode-specific name
2. **Stream Reader**: Sets up a streaming DataFrame to monitor the `data/input` directory
3. **Schema Application**: Applies the predefined schema to incoming CSV files
4. **Real-time Processing**: As new files appear, Spark automatically reads and processes them
5. **Mode-specific Output**:
   - **csv-agg**: Groups events by type and counts occurrences
   - **csv-log**: Displays raw data without aggregation
6. **Console Output**: Displays results to console in real-time

#### Phase 4: Continuous Monitoring

1. **File Watching**: Spark continuously monitors the input directory for new files
2. **Automatic Processing**: New files are automatically detected and processed
3. **Live Updates**: Results update in real-time as new data arrives

### WebSocket Streaming Mode (websocket)

#### Phase 1: Socket Server Setup

1. **External Server**: A socket server (like `nc -lk 9999`) listens on a specified port
2. **Text Input**: Users type messages into the server terminal
3. **Network Transmission**: Messages are sent over TCP to the streaming application

#### Phase 2: Stream Connection

1. **Spark Session**: Creates a Spark session for WebSocket processing
2. **Socket Reader**: Connects to the specified host and port
3. **Schema Detection**: Automatically detects text data schema (single "value" column)
4. **Connection Validation**: Verifies the streaming connection is active

#### Phase 3: Text Processing

1. **Line Reading**: Reads text lines from the socket connection
2. **Word Splitting**: Splits each line into individual words
3. **Word Counting**: Performs real-time word count aggregation
4. **Live Display**: Shows word counts updating as new messages arrive

#### Phase 4: Interactive Analysis

1. **Real-time Input**: Users can type new messages to see immediate processing
2. **Aggregation Updates**: Word counts update dynamically
3. **Stream Monitoring**: Continuous processing of incoming text data

### What WebSocket Mode Offers

**WebSocket streaming provides several advantages:**

1. **Real-time Interaction**: Immediate feedback as you type messages
2. **Network-based Streaming**: Simulates real-world network data sources
3. **Text Analytics**: Learn text processing patterns with Spark
4. **Low Latency**: Direct TCP connection for fast data transmission
5. **Interactive Learning**: Experiment with different text inputs instantly
6. **Production Similarity**: Similar to real-time chat, log, or sensor data streams

## 📊 Sample Output

### CSV Aggregation Mode (`--mode csv-agg`)

When running the stream processor with aggregation, you'll see output like:

```
-------------------------------------------
Batch: 0
-------------------------------------------
+--------+-----+
|   event|count|
+--------+-----+
|   login|   15|
|  logout|   12|
|purchase|   18|
|    view|   20|
+--------+-----+

-------------------------------------------
Batch: 1
-------------------------------------------
+--------+-----+
|   event|count|
+--------+-----+
|   login|   25|
|  logout|   22|
|purchase|   28|
|    view|   30|
+--------+-----+
```

### CSV Log Mode (`--mode csv-log`)

When running in log-only mode, you'll see raw data:

```
-------------------------------------------
Batch: 0
-------------------------------------------
+--------------------+-------+--------+
|           timestamp|user_id|   event|
+--------------------+-------+--------+
|2025-07-15T15:03:...|      3|  logout|
|2025-07-15T15:03:...|      2|   login|
|2025-07-15T15:03:...|      2|    view|
|2025-07-15T15:03:...|      5|purchase|
+--------------------+-------+--------+
```

### WebSocket Mode (`--mode websocket`)

When running WebSocket mode and typing "hello world spark streaming" in the socket server:

```
-------------------------------------------
Batch: 0
-------------------------------------------
+---------+-----+
|     word|count|
+---------+-----+
|    hello|    1|
|    world|    1|
|    spark|    1|
|streaming|    1|
+---------+-----+

-------------------------------------------
Batch: 1 (after typing "spark is amazing")
-------------------------------------------
+---------+-----+
|     word|count|
+---------+-----+
|  amazing|    1|
|    hello|    1|
|       is|    1|
|    spark|    2|
|streaming|    1|
|    world|    1|
+---------+-----+
```

## Configuration Options

This project demonstrates various PySpark Structured Streaming configuration options. For a comprehensive guide covering all available options, see **[`streaming/README.md`](streaming/README.md)**.

### 📖 **What's Covered in the Configuration Guide**

| Section                    | Description                  | Key Topics                                           |
| -------------------------- | ---------------------------- | ---------------------------------------------------- |
| **Reading Data**           | Source configuration options | File sources, Socket sources, Kafka sources          |
| **Schema Configuration**   | Data structure definition    | Explicit schemas, schema inference, DDL strings      |
| **Data Formats**           | Input/output format options  | CSV, JSON, Parquet, Text, Socket, Kafka, Delta       |
| **Aggregation Operations** | Data processing functions    | Basic aggregations, advanced functions, time windows |
| **Output Modes**           | How results are written      | Append, Complete, Update modes                       |
| **Output Formats**         | Destination configuration    | Console, File sinks, Memory, Custom sinks            |
| **Trigger Modes**          | Processing timing control    | Micro-batch, Fixed interval, Once, Available now     |
| **Common Options**         | Essential configurations     | Checkpointing, Query management, Error handling      |
| **Performance Tuning**     | Optimization techniques      | Resource control, Memory management, Monitoring      |

### 🚀 **Quick Configuration Examples**

```python
# Instant processing (no delays)
query = df.writeStream.format("console").start()

# Fixed interval processing
query = df.writeStream.trigger(processingTime='30 seconds').format("console").start()

# File output with checkpointing
query = df.writeStream \
    .option("checkpointLocation", "checkpoints/") \
    .format("parquet") \
    .start()

# Rate limiting for large files
df = spark.readStream \
    .option("maxFilesPerTrigger", 5) \
    .csv("data/input")
```

> 📚 **For complete details, examples, and best practices**, visit [`streaming/README.md`](streaming/README.md)

## Troubleshooting

### Common Issues

1. **Java Not Found Error**

   ```bash
   # Install Java
   brew install openjdk@11

   # Set JAVA_HOME (add to ~/.zshrc)
   export JAVA_HOME=$(/usr/libexec/java_home)
   ```

2. **Python Version Compatibility**

   ```bash
   # Check Python version
   python --version

   # If using Python < 3.10, the Union type hints might cause issues
   # This is already handled in the code
   ```

3. **Port Already in Use**

   ```bash
   # If Spark UI port (4040) is busy, Spark will automatically use 4041, 4042, etc.
   # Check running Spark applications at: http://localhost:4040
   ```

4. **Permission Errors**

   ```bash
   # Ensure write permissions for data directory
   chmod -R 755 data/
   ```

5. **Module Not Found**
   ```bash
   # Make sure you're in the project root and virtual environment is activated
   source venv/bin/activate
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

### Logs and Debugging

- **Loguru logs**: The application uses loguru for logging. Check console output for detailed information
- **Spark UI**: Access the Spark web UI at `http://localhost:4040` for detailed job information
- **Verbose output**: The stream processor shows detailed batch information in the console

---

## Learning Objectives

This project demonstrates:

- **PySpark Structured Streaming** fundamentals and core concepts
- **Real-time data processing** patterns and best practices
- **File-based streaming** (common in data lake scenarios)
- **WebSocket streaming** for network-based real-time data
- **Multiple processing modes** (aggregation vs raw data streaming)
- **CLI-based application design** for flexible streaming configurations
- **Aggregation operations** in streaming context with different output modes
- **Schema enforcement** for data quality and type safety
- **Continuous application** design patterns for production use
- **Error handling and monitoring** for robust streaming applications

### 📚 **Additional Learning Resources**

- **[Configuration Guide](streaming/README.md)**: Comprehensive guide to all PySpark Structured Streaming options
- **[Apache Spark Documentation](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)**: Official structured streaming guide
- **[PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)**: Complete API documentation

Perfect for learning how to build production-ready streaming applications with PySpark! 🚀
