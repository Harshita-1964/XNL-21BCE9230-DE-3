import os

# Set environment variables for Hadoop
os.environ["HADOOP_HOME"] = "C:\\hadoop-3.3.2"
os.environ["PATH"] += "C:\\hadoop-3.3.2\\bin"
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from config import KAFKA_SERVER, KAFKA_TOPIC

spark = SparkSession.builder \
    .appName("SparkStreaming") \
    .config("spark.sql.streaming.checkpointLocation", "checkpoint_dir") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2") \
    .getOrCreate()


schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("amount", IntegerType(), True),
    StructField("type", StringType(), True)
])

kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .load()

transactions_df = kafka_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("transaction")) \
    .select("transaction.*")

query = transactions_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("checkpointLocation", "file:///tmp/spark-checkpoints") \
    .start()

query.awaitTermination()
