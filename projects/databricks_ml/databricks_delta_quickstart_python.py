# Databricks notebook source
table_location = "/mnt/datasetsneugen2/delta/eventsexmaple_py"

# COMMAND ----------

# DBTITLE 1,Read Databricks switch action dataset  
from pyspark.sql.functions import expr
from pyspark.sql.functions import from_unixtime

events = spark.read \
  .option("inferSchema", "true") \
  .json("/databricks-datasets/structured-streaming/events/") \
  .withColumn("date", expr("time")) \
  .drop("time") \
  .withColumn("date", from_unixtime("date", 'yyyy-MM-dd'))
  
display(events)

# COMMAND ----------

# DBTITLE 1,Write out DataFrame as Databricks Delta data
events.write.format("delta").mode("overwrite").partitionBy("date").save(table_location)

# COMMAND ----------

# DBTITLE 1,Query the data file path
events_delta = spark.read.format("delta").load(table_location)

display(events_delta)

# COMMAND ----------

# DBTITLE 1,Create table
display(spark.sql("DROP TABLE IF EXISTS demodb.eventspy"))

# Create a DELTA backed table from delta files on storage by pointing to the files (we register the table as meta data)
display(spark.sql("CREATE TABLE demodb.eventspy USING DELTA LOCATION '/mnt/datasetsneugen2/delta/eventsexmaple_py'"))

# COMMAND ----------

# DBTITLE 1,Query the table
events_delta.count()

# COMMAND ----------

# DBTITLE 1,Visualize data
from pyspark.sql.functions import count
display(events_delta.groupBy("action","date").agg(count("action").alias("action_count")).orderBy("date", "action"))

# COMMAND ----------

# DBTITLE 1,Generate historical data - original data shifted backwards 2 days
historical_events = spark.read \
  .option("inferSchema", "true") \
  .json("/databricks-datasets/structured-streaming/events/") \
  .withColumn("date", expr("time-172800")) \
  .drop("time") \
  .withColumn("date", from_unixtime("date", 'yyyy-MM-dd'))

# COMMAND ----------

# DBTITLE 1,Append historical data
historical_events.write.format("delta").mode("append").partitionBy("date").save(table_location)

# COMMAND ----------

# DBTITLE 1,Visualize final data
display(events_delta.groupBy("action","date").agg(count("action").alias("action_count")).orderBy("date", "action"))

# COMMAND ----------

# DBTITLE 1,Count rows
events_delta.count()

# COMMAND ----------

# DBTITLE 1,Show contents of a partition
dbutils.fs.ls("dbfs:" + table_location + "/date=2016-07-25/")

# COMMAND ----------

display(spark.sql("OPTIMIZE demodb.eventspy"))

# COMMAND ----------

# DBTITLE 1,Show table history
display(spark.sql("DESCRIBE HISTORY demodb.eventspy"))

# COMMAND ----------

# DBTITLE 1,Show table details
display(spark.sql("DESCRIBE DETAIL demodb.eventspy"))

# COMMAND ----------

# DBTITLE 1,Show the table format
display(spark.sql("DESCRIBE FORMATTED demodb.eventspy"))
