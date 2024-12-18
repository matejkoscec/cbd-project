import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract

from src.config import SparkJobConfig

config = SparkJobConfig(sys.argv)

spark = SparkSession.builder.appName("WebLogAnalysis").getOrCreate()

log_df = spark.read.text(config.input_path)

user_agent_counts = log_df.withColumn("user_agent", regexp_extract("value", r'\"[A-Za-z0-9\s\./\(\);]*\"$', 0)) \
    .groupBy("user_agent").count().orderBy("count", ascending=False)

user_agent_counts.write.csv(f"{config.output_path}/{config.name}", header=True)
