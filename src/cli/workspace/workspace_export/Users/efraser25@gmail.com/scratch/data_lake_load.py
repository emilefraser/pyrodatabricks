# Databricks notebook source
# MAGIC %md
# MAGIC ## Load Data Lakes Tables - Batch and Streaming
# MAGIC For the streaming porting, must have data streaming to the topic "demo-message-1".
# MAGIC
# MAGIC *Note: If not working, try changing the GROUP_ID and Consumer Group values to reset

# COMMAND ----------

# MAGIC %md
# MAGIC ### Shared imports and variables
# MAGIC Run this first since most cells below need at least one of these imports or variables

# COMMAND ----------

from pyspark.sql.functions import col, desc, regexp_replace, substring, to_date, from_json, explode, expr
from pyspark.sql.types import StructType, StringType

taxi_zone_path = "/mnt/adlsdemo/nyctaxi/lookups/taxi_zone"
taxi_rate_path = "/mnt/adlsdemo/nyctaxi/lookups/taxi_rate_code"
yellow_delta_path = "/mnt/adlsdemo/nyctaxi/tripdata/yellow_delta"

date_format = "yyyy-MM-dd HH:mm:ss"

# Define a schema that Spark understands. This is one of several ways to do it.
trip_schema = (
  StructType()
    .add('VendorID', 'integer')
    .add('tpep_pickup_datetime', 'string')
    .add('tpep_dropoff_datetime', 'string')
    .add('passenger_count', 'integer')
    .add('trip_distance', 'double')
    .add('RatecodeID', 'integer')
    .add('store_and_fwd_flag', 'string')
    .add('PULocationID', 'integer')
    .add('DOLocationID', 'integer')
    .add('payment_type', 'integer')
    .add('fare_amount', 'double')
    .add('extra', 'double')
    .add('mta_tax', 'double')
    .add('tip_amount', 'double')
    .add('tolls_amount', 'double')
    .add('improvement_surcharge', 'double')
    .add('total_amount', 'double')
)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Simple load of lookup data
# MAGIC Read data from shared databricks folder and save in delta format within Azure Data Lake Storage (ADLS).

# COMMAND ----------

input_df = (
  spark.read
    .option("header","true")
    .option("inferSchema", "true")
    .csv("/databricks-datasets/nyctaxi/taxizone/taxi_zone_lookup.csv") 
  )

df = input_df.withColumnRenamed("service_zone", "ServiceZone")

df.write.format("delta").mode("overwrite").save(taxi_zone_path)

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Batch Load of historical data
# MAGIC Read historical csv data from shared databricks folder and save in delta format within Azure Data Lake Storage (ADLS).

# COMMAND ----------

# If you want to delete the trips table before starting, keep following line uncommented
# dbutils.fs.rm(yellow_delta_path,recurse=True)

input_df = (
  spark.read
    .option("header","true")
    .schema(trip_schema)
    .csv("dbfs:/databricks-datasets/nyctaxi/tripdata/yellow/yellow_tripdata_2019-*")
)

# Take your pick on how to transform, withColumn or SQL Expressions. Only one of these is needed.
# Option A
transformed_df = (
  input_df
    .withColumn("year_month", regexp_replace(substring("tpep_pickup_datetime",1,7), '-', '_'))
    .withColumn("pickup_dt", to_date("tpep_pickup_datetime", date_format)) 
    .withColumn("dropoff_dt", to_date("tpep_dropoff_datetime", date_format))
    .withColumn("tip_pct", col("tip_amount") / col("total_amount"))
)
  
# Option B
transformed_df = input_df.selectExpr(
                  "*",
                  "replace(left(tpep_pickup_datetime, 7),'-','_') as year_month",
                  f"to_date(tpep_pickup_datetime, '{date_format}') as pickup_dt",
                  f"to_date(tpep_dropoff_datetime, '{date_format}') as dropoff_dt",
                  f"tip_amount/total_amount as tip_pct")

zone_df = spark.read.format("delta").load(taxi_zone_path)

# Join to bring in Taxi Zone data
trip_df = (
   transformed_df
     .join(zone_df, transformed_df.PULocationID == zone_df.LocationID, how="left").drop("LocationID")
     .withColumnRenamed("Burough", "PickupBurrough")
     .withColumnRenamed("Zone", "PickupZone")
     .withColumnRenamed("ServiceZone", "PickupServiceZone")
)

trip_df.write.mode("overwrite").partitionBy("year_month").format("delta").save(yellow_delta_path)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Stream Load of incoming data - Trips for 2019-12
# MAGIC Read streaming data from Event Hubs (using Apache Kafka API) and save in the same delta location within Azure Data Lake Storage (ADLS).

# COMMAND ----------

spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")

run_version = "v25"

topic = 'demo-message-1'

# To setup Key Vault backed secret scope for this first time, replace items in url and follow instructions: 
#   https://<databricks-instance>/#secrets/createScopeSetup

# Password is really a Event Hub connection string, for example -> Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=ReadWriteTmp;SharedAccessKey=vhNXxXXXXXxxxXXXXXXXxx=;EntityPath=demo-message-1
password = dbutils.secrets.get(scope = "demo", key = "eh-sasl-{0}".format(topic))

EH_SASL = 'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{0}";'.format(password)
GROUP_ID = f'tst-group-{run_version}'

consumer_config = {
    'kafka.bootstrap.servers': 'dustin-demo-eh.servicebus.windows.net:9093',
    'kafka.security.protocol': 'SASL_SSL',
    'kafka.sasl.mechanism': 'PLAIN',
    'kafka.group.id': GROUP_ID,
    'kafka.request.timeout.ms': "60000",
    'kafka.session.timeout.ms': "20000",
    'kafka.heartbeat.interval.ms': "10000",
    'kafka.sasl.jaas.config': EH_SASL,
    'subscribe': topic
}

# Read from Kafka, format will be a kafka record
input_df = spark.readStream.format("kafka").options(**consumer_config).load()

# Cast just the value as a string (instead of bytes) then use from_json to convert to an object matching the schema
json_df = (
  input_df.select(
    from_json(col('value').cast('string'), trip_schema).alias("json")
  )
)

# Select all attribues from json as individual columns, cast trip_distance, add columns
transformed_df = (
    json_df
      .select("json.*")
      .withColumn("year_month", regexp_replace(substring("tpep_pickup_datetime",1,7), '-', '_'))
      .withColumn("pickup_dt", to_date("tpep_pickup_datetime", date_format)) 
      .withColumn("dropoff_dt", to_date("tpep_dropoff_datetime", date_format))
      .withColumn("tip_pct", col("tip_amount") / col("total_amount"))
)

# Join in lookup data
zone_df = spark.read.format("delta").load(taxi_zone_path)
trip_df = (
   transformed_df
     .join(zone_df, transformed_df["PULocationId"] == zone_df["LocationID"], how="left").drop("LocationID")
     .withColumnRenamed("Burough", "PickupBurrough")
     .withColumnRenamed("Zone", "PickupZone")
     .withColumnRenamed("ServiceZone", "PickupServiceZone")
)

display(trip_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Azure Storage as a destination
# MAGIC * One option for streaming output is to write directly to you data lake storage (Azure Data Lake Storage Gen 2 or standard Azure Blob Storage).
# MAGIC * Databricks Delta / Delta Lake file format makes this more efficient, but could do with Parquet, Avro or other formats.

# COMMAND ----------

(
 trip_df.writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation", f"/delta/events/_checkpoints/streaming_demo_{run_version}")
  .partitionBy("year_month")
  .start(yellow_delta_path)
)

# COMMAND ----------

# delta_batch_df = spark.read.format("delta").load(yellow_delta_path).limit(1000)
# display(delta_batch_df)

delta_stream_df = spark.readStream.format("delta").load(yellow_delta_path).filter(col("tpep_pickup_datetime") == "2019-12-01 00:18:15")
display(delta_stream_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Alternatively: Send transformed data to Event Hubs for next steps in pipeline

# COMMAND ----------

topic2 = 'demo-message-transformed'

password = dbutils.secrets.get("data-lake-demo", "eh-sasl-{0}".format(topic2))

EH_SASL = 'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{0}";'.format(password)

producer_config = {
    'kafka.bootstrap.servers': 'dustin-demo-eh.servicebus.windows.net:9093',
    'kafka.security.protocol': 'SASL_SSL',
    'kafka.sasl.mechanism': 'PLAIN',
    'kafka.request.timeout.ms': "60000",
    'kafka.session.timeout.ms': "30000",
    'kafka.sasl.jaas.config': EH_SASL,
    'topic': topic2
}

kafka_output_df = trip_df.selectExpr(
    "CAST(VendorId as STRING) as key",
    "to_json(struct(*)) as value")

# display(kafka_output_df)
kafka_output_df.writeStream \
  .format("kafka") \
  .options(**producer_config) \
  .option("checkpointLocation", f"/delta/events/_checkpoints/cp_{run_version}") \
  .start()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tests and other alternative syntax
# MAGIC Collection of examples not used in demo but show other capabilities and syntax.

# COMMAND ----------

# Exmaple of grouping the data in a stream, which requires defining a window

# from pyspark.sql.functions import window  

# grouped_df = (
#       trips2_df
#         .groupBy(
#            col("passenger_count"),
#            window("tpep_pickup_datetime", "10 minutes"))
#         .sum("trip_distance")
#       )

# # display(grouped_df)

# COMMAND ----------

# # Example to get actual json schema from sample file (avoid typing it all manually)
# file_location = "/mnt/blobdemo/nyc_taxi_raw/yellow_tripdata_2018-01.csv"
# sample_df = spark.read \
#     .option('sep',',') \
#     .option("inferSchema","true") \
#     .option("header", "true") \
#     .csv(file_location)
# json_schema = sample_df.schema

# COMMAND ----------

transformed_df = spark.read.format("delta").load(yellow_delta_path).limit(1000)
zone_df = spark.read.format("delta").load(taxi_zone_path)
trip_df = transformed_df.join(zone_df, transformed_df.PULocationID == zone_df.LocationID, how="left").drop("LocationID")
display(trip_df)

# COMMAND ----------

GROUP_ID = f"test-group-2-{run_version}"
consumer2_config = {
    'kafka.bootstrap.servers': 'dustin-demo-eh.servicebus.windows.net:9093',
    'kafka.security.protocol': 'SASL_SSL',
    'kafka.sasl.mechanism': 'PLAIN',
    'kafka.request.timeout.ms': "60000",
    'kafka.session.timeout.ms': "20000",
    'kafka.sasl.jaas.config': EH_SASL,
    'kafka.group.id': GROUP_ID,
    'subscribe': topic2
}

df3 = spark.readStream \
    .format("kafka") \
    .options(**consumer2_config) \
    .load()

df3 = df3.select(col("value").cast("string"))

# display(df3)

# COMMAND ----------

# output_path = f"/mnt/adlsdemo/streaming_output_{run_version}"

# delta_stream_df = spark.readStream.format("delta").load(output_path)
# delta_stream_df.writeStream.format("delta").option("checkpointLocation", "/mnt/adlsdemo/checkpoints/demo_v1").start(output_path+"2")
#  display(delta_stream_df)

# COMMAND ----------

df = (
  spark.read
    .option("header","true")
    .option("inferSchema", "true")
    .csv("/databricks-datasets/nyctaxi/taxizone/taxi_rate_code.csv") 
  )

df.write.format("delta").mode("overwrite").save(taxi_rate_path)

display(df)

# COMMAND ----------

input_df = (
  spark.read
    .option("header","true")
    .schema(trip_schema)
    .csv("dbfs:/databricks-datasets/nyctaxi/tripdata/yellow/yellow_tripdata_2019-12.csv.gz")
)

input_df.coalesce(1).write.json("dbfs:/data/nyctaxi/december_json")

# COMMAND ----------

# MAGIC %fs ls /mnt/adlsdemo/streaming_output_v20/

# COMMAND ----------

# MAGIC %md
# MAGIC #### Possible error  
# MAGIC Caused by: org.apache.spark.SparkUpgradeException: You may get a different result due to the upgrading of Spark 3.0: Fail to recognize 'YYYY-MM-dd hh:mm:ss' pattern in the DateTimeFormatter. 1) You can set spark.sql.legacy.timeParserPolicy to LEGACY to restore the behavior before Spark 3.0. 2) You can form a valid datetime pattern with the guide from https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html