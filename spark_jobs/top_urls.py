import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract

from src.config import SparkJobConfig

config = SparkJobConfig(sys.argv)

spark = SparkSession.builder.appName("WebLogAnalysis").getOrCreate()

log_df = spark.read.text(config.input_path)

url_counts = log_df.withColumn("url", regexp_extract("value", r'\"GET (.*?) HTTP/1.1\"', 1)) \
    .groupBy("url").count().orderBy("count", ascending=False)

url_counts.write.csv(f"{config.output_path}/{config.name}", header=True)
