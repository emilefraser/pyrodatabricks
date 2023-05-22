# Databricks notebook source
# MAGIC %scala
# MAGIC 
# MAGIC val df = spark.read.format("json")
# MAGIC .load("/databricks-datasets/definitive-guide/data/flight-data/json/2015-summary.json")

# COMMAND ----------

# MAGIC %python
# MAGIC 
# MAGIC df = spark.read.format("json") \
# MAGIC .load("/databricks-datasets/definitive-guide/data/flight-data/json/2015-summary.json")

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC import org.apache.spark.sql.functions.{expr, col, column}
# MAGIC 
# MAGIC df.select(
# MAGIC   df.col("DEST_COUNTRY_NAME"),
# MAGIC   col("DEST_COUNTRY_NAME"),
# MAGIC   column("DEST_COUNTRY_NAME"),
# MAGIC   'DEST_COUNTRY_NAME,
# MAGIC   $"DEST_COUNTRY_NAME",
# MAGIC   expr("DEST_COUNTRY_NAME")
# MAGIC ).show(2)

# COMMAND ----------

# MAGIC %python
# MAGIC from pyspark.sql.functions import expr, col, column
# MAGIC 
# MAGIC df.select(
# MAGIC   expr("DEST_COUNTRY_NAME"),
# MAGIC   col("DEST_COUNTRY_NAME"),
# MAGIC   df["DEST_COUNTRY_NAME"],
# MAGIC   df.DEST_COUNTRY_NAME,
# MAGIC   "DEST_COUNTRY_NAME"
# MAGIC ).show(2)

# COMMAND ----------

# MAGIC %scala
# MAGIC // and python
# MAGIC 
# MAGIC df.select(expr("DEST_COUNTRY_NAME AS destination")).show(2)

# COMMAND ----------

df.select(
  expr("DEST_COUNTRY_NAME as destination").alias("DEST_COUNTRY_NAME")
).show(2)

df.selectExpr(
  "DEST_COUNTRY_NAME as destination", 
  "DEST_COUNTRY_NAME"
).show(2)

df.selectExpr(
  "*",
  "(DEST_COUNTRY_NAME = ORIGIN_COUNTRY_NAME) as withinCountry"
).show(2)

df.selectExpr(
  "avg(count)", 
  "count(distinct(DEST_COUNTRY_NAME))"
).show(2)

import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('cgpysparklabs').getOrCreate()

data = [("James","Smith","US","CA"),
... ("Michael","Rose","US","NY"),
... ("Robert","William","UK","London"),
... ("Maria","Brown","US","FL")]
columns = ["firstname","lastname","country","state"]
df = spark.createDataFrame(data=data,schema=columns)
df.show(truncate=False)
+---------+--------+-------+------+
|firstname|lastname|country|state |
+---------+--------+-------+------+
|James    |Smith   |US     |CA    |
|Michael  |Rose    |US     |NY    |
|Robert   |William |UK     |London|
|Maria    |Brown   |US     |FL    |
+---------+--------+-------+------+

df.select("firstname","lastname").show()
+---------+--------+
|firstname|lastname|
+---------+--------+
|    James|   Smith|
|  Michael|    Rose|
|   Robert| William|
|    Maria|   Brown|
+---------+--------+

df.select(df.firstname,df.lastname).show()
+---------+--------+
|firstname|lastname|
+---------+--------+
|    James|   Smith|
|  Michael|    Rose|
|   Robert| William|
|    Maria|   Brown|
+---------+--------+

df.select(df["firstname"],df["lastname"]).show()
+---------+--------+
|firstname|lastname|
+---------+--------+
|    James|   Smith|
|  Michael|    Rose|
|   Robert| William|
|    Maria|   Brown|
+---------+--------+

from pyspark.sql.functions import col
df.select(col("firstname"),col("lastname")).show()
+---------+--------+
|firstname|lastname|
+---------+--------+
|    James|   Smith|
|  Michael|    Rose|
|   Robert| William|
|    Maria|   Brown|
+---------+--------+


df.select(*columns).show()
+---------+--------+-------+------+
|firstname|lastname|country| state|
+---------+--------+-------+------+
|    James|   Smith|     US|    CA|
|  Michael|    Rose|     US|    NY|
|   Robert| William|     UK|London|
|    Maria|   Brown|     US|    FL|
+---------+--------+-------+------+

df.select([col for col in df.columns]).show()
+---------+--------+-------+------+
|firstname|lastname|country| state|
+---------+--------+-------+------+
|    James|   Smith|     US|    CA|
|  Michael|    Rose|     US|    NY|
|   Robert| William|     UK|London|
|    Maria|   Brown|     US|    FL|
+---------+--------+-------+------+

df.select("*").show()
+---------+--------+-------+------+
|firstname|lastname|country| state|
+---------+--------+-------+------+
|    James|   Smith|     US|    CA|
|  Michael|    Rose|     US|    NY|
|   Robert| William|     UK|London|
|    Maria|   Brown|     US|    FL|
+---------+--------+-------+------+

df.select(df.columns[:3]).show(3)
+---------+--------+-------+
|firstname|lastname|country|
+---------+--------+-------+
|    James|   Smith|     US|
|  Michael|    Rose|     US|
|   Robert| William|     UK|
+---------+--------+-------+
#only showing top 3 rows

df.select(df.columns[2:4]).show(3)
+-------+------+
|country| state|
+-------+------+
|     US|    CA|
|     US|    NY|
|     UK|London|
+-------+------+
#only showing top 3 rows

