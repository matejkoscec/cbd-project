import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract

from src.config import SparkJobConfig

config = SparkJobConfig(sys.argv)

spark = SparkSession.builder.appName("WebLogAnalysis").getOrCreate()

log_df = spark.read.text(config.input_path)

status_code_counts = log_df.withColumn("status_code", regexp_extract("value", r'\" (\d{3}) ', 1)) \
    .groupBy("status_code").count().orderBy("count", ascending=False)

status_code_counts.write.csv(f"{config.output_path}/{config.name}", header=True)
