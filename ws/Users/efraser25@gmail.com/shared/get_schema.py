# Databricks notebook source
# MAGIC %md
# MAGIC ## Prints out schema to screen

# COMMAND ----------

df = spark.read.load("/mnt/bronze/project=lotto/source=master_data")
display(df)
df.printSchema()