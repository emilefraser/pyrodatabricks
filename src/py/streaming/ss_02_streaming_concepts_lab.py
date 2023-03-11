# Databricks notebook source
# MAGIC 
# MAGIC %md-sandbox
# MAGIC 
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px; height: 163px">
# MAGIC </div>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <img src="https://files.training.databricks.com/images/Apache-Spark-Logo_TM_200px.png" style="float: left: margin: 20px"/>
# MAGIC 
# MAGIC # Structured Streaming Concepts Lab
# MAGIC 
# MAGIC ## Instructions
# MAGIC * Insert solutions wherever it says `FILL_IN`
# MAGIC * Feel free to copy/paste code from the previous notebook, where applicable
# MAGIC * Run test cells to verify that your solution is correct
# MAGIC 
# MAGIC ## Prerequisites
# MAGIC * Web browser: **Chrome**
# MAGIC * A cluster configured with **8 cores** and **DBR 6.2**
# MAGIC * Suggested Courses from <a href="https://academy.databricks.com/" target="_blank">Databricks Academy</a>:
# MAGIC   - ETL Part 1
# MAGIC   - Spark-SQL

# COMMAND ----------

# MAGIC %md
# MAGIC ## ![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) Classroom-Setup
# MAGIC 
# MAGIC For each lesson to execute correctly, please make sure to run the **`Classroom-Setup`** cell at the<br/>
# MAGIC start of each lesson (see the next cell) and the **`Classroom-Cleanup`** cell at the end of each lesson.

# COMMAND ----------

# MAGIC %run "../Includes/Classroom-Setup"

# COMMAND ----------

# MAGIC %md
# MAGIC Define the name of the stream we are to use later in this lesson:

# COMMAND ----------

myStreamName = "lab02_ps"

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC <h2><img src="https://files.training.databricks.com/images/105/logo_spark_tiny.png"> Exercise 1: Read Stream</h2>
# MAGIC 
# MAGIC The dataset used in this exercise consists of flight information about flights from/to various airports in 2007.
# MAGIC 
# MAGIC Run the following cell to see what the streaming data will look like.

# COMMAND ----------

display(
  spark.read.parquet("dbfs:/mnt/training/asa/flights/2007-01-stream.parquet/part-00000-tid-9167815511861375854-22d81a30-d5b4-43d0-9216-0c20d14c3f54-178-c000.snappy.parquet")
)

# COMMAND ----------

# MAGIC %md
# MAGIC Start by reading a stream. 
# MAGIC 
# MAGIC For this step you will need to:
# MAGIC 0. Starting with `spark`, an instance of `SparkSession`, and get the `DataStreamReader`
# MAGIC 0. Make sure to only consume only 1 file per trigger
# MAGIC 0. Specify the stream's schema using the instance `dataSchema` (already provided for you)
# MAGIC 0. Use `dsr.parquet()` to specify the stream's file type and source directory, `dataPath` 
# MAGIC 
# MAGIC When you are done, run the TEST cell that follows to verify your results.

# COMMAND ----------

# ANSWER
dataSchema = "DepartureAt timestamp, FlightDate string, DepTime string, CRSDepTime string, ArrTime string, CRSArrTime string, UniqueCarrier string, FlightNum integer, TailNum string, ActualElapsedTime string, CRSElapsedTime string, AirTime string, ArrDelay string, DepDelay string, Origin string, Dest string, Distance string, TaxiIn string, TaxiOut string, Cancelled integer, CancellationCode string, Diverted integer, CarrierDelay string, WeatherDelay string, NASDelay string, SecurityDelay string, LateAircraftDelay string"

dataPath = "dbfs:/mnt/training/asa/flights/2007-01-stream.parquet"

initialDF = (spark
  .readStream                       # Get a DataStreamReader
  .option("maxFilesPerTrigger", 1)  # Force processing of only 1 file per trigger 
  .schema(dataSchema)               # Use the schema "dataSchema"
  .parquet(dataPath)                # Read in stream's file type and source directory
)

# COMMAND ----------

# TEST - Run this cell to test your solution.
schemaStr = str(initialDF.schema)

dbTest("SS-02-schema-01", True, "(DepartureAt,TimestampType,true)" in schemaStr) 
dbTest("SS-02-schema-02", True, "(FlightDate,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-03", True, "(DepTime,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-04", True, "(CRSDepTime,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-05", True, "(ArrTime,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-06", True, "(CRSArrTime,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-07", True, "(UniqueCarrier,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-08", True, "(FlightNum,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-09", True, "(TailNum,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-10", True, "(ActualElapsedTime,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-11", True, "(CRSElapsedTime,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-12", True, "(AirTime,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-13", True, "(ArrDelay,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-14", True, "(DepDelay,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-15", True, "(Origin,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-16", True, "(Dest,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-17", True, "(Distance,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-18", True, "(TaxiIn,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-19", True, "(TaxiOut,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-20", True, "(Cancelled,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-21", True, "(CancellationCode,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-22", True, "(Diverted,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-23", True, "(CarrierDelay,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-24", True, "(WeatherDelay,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-25", True, "(NASDelay,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-26", True, "(SecurityDelay,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-27", True, "(LateAircraftDelay,StringType,true)" in schemaStr) 

print("Tests passed!")

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC 
# MAGIC <h2><img src="https://files.training.databricks.com/images/105/logo_spark_tiny.png"> Exercise 2: Calculate the total of all delays</h2>
# MAGIC 
# MAGIC We want to calculate (and later graph) the total delay of each flight
# MAGIC 0. Start with `initialDF` from the previous exercise 
# MAGIC 0. Convert the following columns from `String` to `Integer`: `CarrierDelay`, `WeatherDelay`, `NASDelay`, `SecurityDelay` and `LateAircraftDelay`
# MAGIC 0. Add the column `TotalDelay` which is the sum of the other 5 delays
# MAGIC 0. Filter the flights by `UniqueCarrier` down to the carriers **AS**, **AQ**, **HA** and **F9**
# MAGIC 0. Filter the results to non-zero delay's (`TotalDelay` > 0)
# MAGIC 0. Assign the final DataFrame to `delaysDF`
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> The `display()` function will only plot the first 1000 records. By limiting ourselves to four carriers and non-zero delays, we can help to ensure that we get a reasonable demonstration of a live plot.

# COMMAND ----------

# ANSWER
from pyspark.sql.functions import col

delaysDF = (initialDF
  .withColumn("CarrierDelay", col("CarrierDelay").cast("integer"))
  .withColumn("WeatherDelay", col("WeatherDelay").cast("integer"))
  .withColumn("NASDelay", col("NASDelay").cast("integer"))
  .withColumn("SecurityDelay", col("SecurityDelay").cast("integer"))
  .withColumn("LateAircraftDelay", col("LateAircraftDelay").cast("integer"))
  .withColumn("TotalDelay", col("CarrierDelay") + col("WeatherDelay") + col("NASDelay") + col("SecurityDelay") + col("LateAircraftDelay"))
  .filter(col("UniqueCarrier").isin("AS", "AQ", "HA", "F9"))
  .filter(col("TotalDelay") > 0)
)

# COMMAND ----------

# TEST - Run this cell to test your solution.
schemaStr = str(delaysDF.schema)

dbTest("SS-02-schema-01", True, "(UniqueCarrier,StringType,true)" in schemaStr) 
dbTest("SS-02-schema-02", True, "(TotalDelay,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-03", True, "(CarrierDelay,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-04", True, "(WeatherDelay,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-05", True, "(NASDelay,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-06", True, "(SecurityDelay,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-07", True, "(LateAircraftDelay,IntegerType,true)" in schemaStr) 
dbTest("SS-02-schema-08", True, "(DepartureAt,TimestampType,true)" in schemaStr) 

print("Tests passed!")

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC <h2><img src="https://files.training.databricks.com/images/105/logo_spark_tiny.png"> Exercise 3: Plot a LIVE graph</h2>
# MAGIC 
# MAGIC Plot `delaysDF` and give the stream the name "delays_python"
# MAGIC 
# MAGIC Once the data is loaded, render a line graph with 
# MAGIC * **Keys** is set to `DepartureAt`
# MAGIC * **Series groupings** is set to `UniqueCarrier`
# MAGIC * **Values** is set to `TotalDelay`
# MAGIC 
# MAGIC <img alt="Side Note" title="Side Note" style="vertical-align: text-bottom; position: relative; height:1.75em; top:0.05em; transform:rotate(15deg)" src="https://files.training.databricks.com/static/images/icon-note.webp"/> Because of the `display()` function's 1000 record limit, the stream will appear to stop shortly after January 5th.

# COMMAND ----------

# ANSWER
display(delaysDF, streamName = myStreamName)

# COMMAND ----------

# TEST - Run this cell to test your solution.
count = 0
for s in spark.streams.active:
  if (s.name == myStreamName):
    count = count + 1

dbTest("SS-02-runningCount", 1, count)

print("Tests passed!")

# COMMAND ----------

# MAGIC %md
# MAGIC When you are done, stop the stream:

# COMMAND ----------

stopAllStreams()

# COMMAND ----------

# MAGIC %md
# MAGIC <h2><img src="https://files.training.databricks.com/images/105/logo_spark_tiny.png"> Exercise 4: Write Stream</h2>
# MAGIC 
# MAGIC Write the stream to an in-memory table
# MAGIC 0. Use appropriate `format`
# MAGIC 0. For this exercise, we want to append new records to the results table
# MAGIC 0. Configure a 15 second trigger
# MAGIC 0. Name the query "delays_python"
# MAGIC 0. Start the query
# MAGIC 0. Assign the query to `delayQuery`

# COMMAND ----------

# ANSWER
delayQuery = (delaysDF 
 .writeStream                           # From the DataFrame get the DataStreamWriter
 .format("memory")                      # Specify the sink format as "memory"
 .outputMode("append")                  # Configure the output mode as "append"
 .queryName(myStreamName)               # Name the query with myStreamName
 .trigger(processingTime="15 seconds")  # Use a 15 second trigger
 .start()                               # Start the query
)

# COMMAND ----------

# TEST - Run this cell to test your solution.
dbTest("SS-02-isActive", True, delayQuery.isActive)
dbTest("SS-02-name", myStreamName, delayQuery.name)
# The query's trigger is not available via the Python API

print("Tests passed!")

# COMMAND ----------

# MAGIC %md
# MAGIC Wait until stream is done initializing...

# COMMAND ----------

untilStreamIsReady(myStreamName)

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC <h2><img src="https://files.training.databricks.com/images/105/logo_spark_tiny.png"> Exercise 5: Stop streaming jobs</h2>
# MAGIC 
# MAGIC Before we can conclude, we need to shut down all active streams.

# COMMAND ----------

# ANSWER
for s in spark.streams.active: # Iterate over all active streams
  try:
    print("stopping " + s.name)  # A little console output
    s.stop()                     # Stop the stream

  except Exception as e:
    # In extream cases, this funtion may throw an ignorable error.
    print("An [ignorable] error has occured while stoping the stream.\n".str(e))
    

# COMMAND ----------

# TEST - Run this cell to test your solution.
dbTest("SS-02-numActiveStreams", 0, len(spark.streams.active))

print("Tests passed!")

# COMMAND ----------

# MAGIC %md
# MAGIC ## ![Spark Logo Tiny](https://files.training.databricks.com/images/105/logo_spark_tiny.png) Classroom-Cleanup<br>
# MAGIC 
# MAGIC Run the **`Classroom-Cleanup`** cell below to remove any artifacts created by this lesson.

# COMMAND ----------

# MAGIC %run "../Includes/Classroom-Cleanup"

# COMMAND ----------

# MAGIC %md
# MAGIC <h2><img src="https://files.training.databricks.com/images/105/logo_spark_tiny.png"> Next Steps</h2>
# MAGIC 
# MAGIC Start the next lesson, [Time Windows]($../SS 03 - Time Windows).

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2020 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/>
# MAGIC <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>