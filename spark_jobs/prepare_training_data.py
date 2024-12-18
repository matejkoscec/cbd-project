import sys

from pyspark.ml.feature import StringIndexer
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, split, col, length

from src.config import SparkJobConfig

spark = SparkSession.builder \
    .appName("LogParser") \
    .config("spark.executor.memory", "8g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.kryoserializer.buffer.max", "512m") \
    .getOrCreate()

config = SparkJobConfig(sys.argv)

logs_df = spark.read.text(config.input_path).toDF("raw")

log_pattern = r'^(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]*)" (\d{3}) (\S+) "([^"]*)" "([^"]*)"'

parsed_df = logs_df.select(
    regexp_extract("raw", log_pattern, 1).alias("ip"),
    regexp_extract("raw", log_pattern, 2).alias("ident"),
    regexp_extract("raw", log_pattern, 3).alias("authuser"),
    regexp_extract("raw", log_pattern, 4).alias("datetime"),
    regexp_extract("raw", log_pattern, 5).alias("request"),
    regexp_extract("raw", log_pattern, 6).alias("status"),
    regexp_extract("raw", log_pattern, 7).alias("bytes"),
    regexp_extract("raw", log_pattern, 8).alias("referrer"),
    regexp_extract("raw", log_pattern, 9).alias("useragent")
)

parsed_df = parsed_df.withColumn("method", split(col("request"), " ").getItem(0)) \
    .withColumn("endpoint", split(col("request"), " ").getItem(1)) \
    .withColumn("protocol", split(col("request"), " ").getItem(2))

parsed_df = parsed_df.withColumn("status", col("status").cast("integer")) \
    .withColumn("bytes", col("bytes").cast("integer"))

parsed_df = parsed_df.withColumn("endpoint_length", length(col("endpoint")))

method_indexer = StringIndexer(inputCol="method", outputCol="method_index")
parsed_df = method_indexer.fit(parsed_df).transform(parsed_df)

final_df = parsed_df.select("status", "bytes", "endpoint_length", "method_index")

final_df.write.csv(f"{config.output_path}/{config.name}", header=True)

spark.stop()
