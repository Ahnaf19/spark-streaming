# PySpark Structured Streaming from CSV

This project demonstrates real-time data processing using PySpark Structured Streaming. It simulates a continuous data stream by generating CSV files and processes them in real-time to perform aggregations and transformations.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [What's Happening Step by Step](#whats-happening-step-by-step)
- [Understanding the Code](#understanding-the-code)
- [Sample Output](#sample-output)
- [Troubleshooting](#troubleshooting)

> [!NOTE]
> Developed on `python 3.10.16`.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Spark](https://img.shields.io/badge/spark-E25A1C?style=for-the-badge&logo=apache-spark&logoColor=white) ![Loguru](https://img.shields.io/badge/loguru-FF9C00?style=for-the-badge&logo=python&logoColor=white) ![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

## 🎯 Overview

This project simulates a real-world streaming scenario where:

1. **Data Generator**: Continuously generates CSV files with user event data (login, logout, purchase, view)
2. **Stream Processor**: Uses PySpark Structured Streaming to monitor the input directory and process new files in real-time
3. **Real-time Analytics**: Performs aggregations (counting events by type) and displays results to the console

## 📁 Project Structure

```
spark-streaming/
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── data/
│   └── input/                   # Directory where CSV files are generated
│       ├── event_batch_0.csv    # Sample event data files
│       ├── event_batch_1.csv
│       └── ...
├── generator/
│   └── csv_writer.py           # Script to generate CSV files
├── schema/
│   ├── __init__.py
│   └── csv_schema.py           # PySpark schema definition
└── streaming/
    └── stream_processor.py     # Main streaming application
```

## 🔧 Prerequisites

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

## 🚀 Setup Instructions

### 1. Clone or Download the Repository

```bash
# If using git
git clone <repository-url>
cd spark-streaming

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

## 🏃‍♂️ Running the Project

### Method 1: Automated Run (Recommended)

1. **Terminal 1 - Start the Stream Processor:**

```bash
cd spark-streaming
python streaming/stream_processor.py
```

2. **Terminal 2 - Generate Data:**

```bash
cd spark-streaming
python generator/csv_writer.py
```

### Method 2: Manual Step-by-Step

1. **Generate some initial data:**

```bash
python generator/csv_writer.py
```

2. **Start the streaming processor:**

```bash
python streaming/stream_processor.py
```

3. **Generate more data** (in another terminal) to see real-time processing:

```bash
python generator/csv_writer.py
```

### Stopping the Application

- Press `Ctrl+C` in the stream processor terminal to stop the streaming query
- The data generator will stop automatically after creating 10 files

## 📚 What's Happening Step by Step

### Phase 1: Data Generation

1. **CSV Writer Initialization**: The `csv_writer.py` script creates the `data/input` directory
2. **File Generation**: Generates 10 CSV files (`event_batch_0.csv` to `event_batch_9.csv`) with a 3-second delay between each
3. **Data Structure**: Each file contains 10 rows of simulated user events with:
   - `timestamp`: Current datetime in ISO format
   - `user_id`: Random integer between 1-5
   - `event`: Random choice from ["login", "logout", "purchase", "view"]

### Phase 2: Schema Definition

1. **Schema Setup**: The `csv_schema.py` defines the structure of incoming data
2. **Type Safety**: Ensures PySpark knows the data types (timestamp as string, user_id as integer, event as string)

### Phase 3: Stream Processing

1. **Spark Session**: Creates a Spark session named "CSVStreamProcessor"
2. **Stream Reader**: Sets up a streaming DataFrame to monitor the `data/input` directory
3. **Schema Application**: Applies the predefined schema to incoming CSV files
4. **Real-time Processing**: As new files appear, Spark automatically reads and processes them
5. **Aggregation**: Groups events by type and counts occurrences
6. **Output**: Displays results to console in real-time

### Phase 4: Continuous Monitoring

1. **File Watching**: Spark continuously monitors the input directory for new files
2. **Automatic Processing**: New files are automatically detected and processed
3. **Live Updates**: Aggregation results update in real-time as new data arrives

## 🔍 Understanding the Code

### Data Generator (`generator/csv_writer.py`)

```python
def generate_csv(file_index, rows=10):
    # Creates CSV files with random event data
    # Each file has 10 rows of timestamp, user_id, event data
```

### Schema Definition (`schema/csv_schema.py`)

```python
schema = StructType() \
    .add("timestamp", StringType()) \
    .add("user_id", IntegerType()) \
    .add("event", StringType())
```

### Stream Processor (`streaming/stream_processor.py`)

```python
# Read stream from CSV files
df = spark.readStream \
    .option("header", True) \
    .schema(schema) \
    .csv("data/input")

# Aggregate data by event type
agg = df.groupBy("event").count()

# Output to console
query = agg.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()
```

## 📊 Sample Output

When running the stream processor, you'll see output like:

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

## 🛠️ Troubleshooting

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

## 🎓 Learning Objectives

This project demonstrates:

- **PySpark Structured Streaming** fundamentals
- **Real-time data processing** patterns
- **File-based streaming** (common in data lake scenarios)
- **Aggregation operations** in streaming context
- **Schema enforcement** for data quality
- **Continuous application** design patterns

Perfect for learning how to build production-ready streaming applications with PySpark!
