from pyspark.sql.types import StructType, StringType, IntegerType


schema = StructType() \
    .add("timestamp", StringType()) \
    .add("user_id", IntegerType()) \
    .add("event", StringType())