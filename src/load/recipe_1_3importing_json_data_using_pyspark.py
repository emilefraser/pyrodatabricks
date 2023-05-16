# Databricks notebook source
# MAGIC %sql
# MAGIC create table sample;

# COMMAND ----------

# DBTITLE 1,Reading multiple JSON files at the same time
df = (
  spark.read
       .option('inferSchema', 'true')
       .json("/mnt/00-mchan-demo/databricks-cookbook/ch01_r03/v1")
)

display(df)

# COMMAND ----------

# DBTITLE 1,Reading multi-line JSON
df = (
  spark.read
       .format("json")
       .option("multiline", "true")
       .load("/mnt/00-mchan-demo/databricks-cookbook/ch01_r03/v2")
)

display(df)

# COMMAND ----------

# DBTITLE 1,Reading JSON Files with a user-specified schema 
from pyspark.sql.types import * 

schema = StructType(
  [
    StructField("reading_date", TimestampType()),
    StructField("row_id", IntegerType()),
    StructField("sensor", StringType()),    
    StructField("temperature", FloatType())    
  ]
)

df = (
  spark.read
       .format("json")
       .option("multiline","true")
       .schema(schema)
       .load("/mnt/00-mchan-demo/databricks-cookbook/ch01_r03/v2")
)

display(df)

# COMMAND ----------

df.printSchema()
