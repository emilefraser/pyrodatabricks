-- Databricks notebook source
-- MAGIC %md
-- MAGIC # SQL Only Interaction
-- MAGIC ## NYC Yellow Trips examples
-- MAGIC This notebooks demonstrates how standard SQL can be used to interact with a data lake.
-- MAGIC This is the recommended starting point for many data scientists and analysts to work with a data lake when Azure Databricks is an option
-- MAGIC
-- MAGIC This notebook and examples on how to mount ADLS and copy code into a mounted ADLS folder are avilable at https://github.com/datakickstart/databricks-notebooks

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Create External Table (schema on read)
-- MAGIC This shows creating a schema on top of a folder of csv files. This data is available at "dbfs:/databricks-datasets/nyctaxi/tripdata/yellow/" though in this example just 2019 was copied into a folder on Azure Data Lake Storage (Gen 2).

-- COMMAND ----------

-- Add schema on top of gzipped csv files in Azure Data Lake Storage (Gen 2) folder
DROP TABLE IF EXISTS trips_external_csv;

CREATE EXTERNAL TABLE trips_external_csv
(
VendorID int,
tpep_pickup_datetime string,
tpep_dropoff_datetime string,
passenger_count int,
trip_distance float,
RatecodeID int,
store_and_fwd_flag string,
PULocationID int,
DOLocationID int,
payment_type int,
fare_amount float,
extra float,
mta_tax float,
tip_amount int,
tolls_amount int,
improvement_surcharge float,
total_amount float,
congestion_surcharge string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1")
LOCATION "/mnt/adlsdemo/nyctaxi/tripdata/yellow/2019"

-- Original location - 1.6 Billion records
-- LOCATION "dbfs:/databricks-datasets/nyctaxi/tripdata/yellow"
-- Just one file for testing
-- LOCATION "dbfs:/databricks-datasets/nyctaxi/tripdata/yellow/yellow_tripdata_2019-12.csv.gz"


-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Query external table
-- MAGIC Examples showing queries against the external table. Notice that a simple count is going to take 10-20 seconds or more. It doesn't make use of statistics like other formats and instead scans through all data to get the row count. Without gzip compression the wait would be even longer.

-- COMMAND ----------

SELECT count(1) from trips_external_csv;

-- COMMAND ----------

SELECT * 
FROM trips_external_csv
WHERE tpep_pickup_datetime > '2019-10-01'
LIMIT 10;

-- COMMAND ----------

DESCRIBE trips_external_csv

-- COMMAND ----------

-- MAGIC %fs ls /mnt/adlsdemo/nyctaxi/tripdata/yellow/2019

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Create Delta Lake table
-- MAGIC Create a Delta Lake table based on external table, just add a bit of partitioning and timestamp conversion.

-- COMMAND ----------

-- Create delta table based on external table
DROP TABLE IF EXISTS yellow_trips_delta;

CREATE TABLE yellow_trips_delta USING DELTA PARTITIONED BY (year_month)
Select replace(left(tpep_pickup_datetime, 7),'-','_') as year_month, * from trips_external_csv;


-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Query Delta Lake table
-- MAGIC Examples showing queries against a delta format table. Notice that query responses will be faster than in our external table. In addition, delta format offers quite a few other features that most data lake file formats don't support.

-- COMMAND ----------

select * from yellow_trips_delta limit 10;


-- COMMAND ----------

SELECT 
  payment_type,
  count(1) record_count,
  avg(tip_amount) avg_tip
FROM yellow_trips_delta
WHERE payment_type is not null
and year_month='2018_12'
GROUP BY payment_type
ORDER BY record_count desc

-- COMMAND ----------

-- MAGIC %fs ls /mnt/adlsdemo/nyctaxi/tripdata/yellow/2019

-- COMMAND ----------

-- MAGIC %fs ls user/hive/warehouse/yellow_trips_delta/