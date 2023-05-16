# Databricks notebook source
# DBTITLE 1,Ingest the data 
s3Path = "/mnt/00-mchan-demo/databricks-cookbook/ch01_r01/"

df = (
  spark.read
       .format("csv")
       .option("inferSchema", "true")
       .option("header", "true")
       .option("pathGlobFilter", "pos*")
       .load(s3Path)
)

display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

(
df.write
  .format("delta")
  .mode("overwrite")
  .saveAsTable("default.t1_bronze_pos_sales")
)
