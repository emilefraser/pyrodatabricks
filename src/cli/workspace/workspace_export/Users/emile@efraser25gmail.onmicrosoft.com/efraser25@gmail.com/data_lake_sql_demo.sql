-- Databricks notebook source
-- MAGIC %md
-- MAGIC # SQL Only Interaction
-- MAGIC This notebooks demonstrates how standard SQL can be used to interact with a data lake.
-- MAGIC This is the recommended starting point for many data scientists and analysts to work with a data lake when Azure Databricks is an option

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Million Songs examples
-- MAGIC Available by default in Azure Databricks.  
-- MAGIC
-- MAGIC http://millionsongdataset.com/
-- MAGIC from original source:
-- MAGIC http://www.columbia.edu/~tb2332/Papers/ismir11.pdf  
-- MAGIC Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
-- MAGIC The Million Song Dataset. In Proceedings of the 12th International Society
-- MAGIC for Music Information Retrieval Conference (ISMIR 2011), 2011.

-- COMMAND ----------

SELECT count(1) from million_songs;

-- COMMAND ----------

SELECT 
  time_signature,
  key,
  artist_name,
  count(1) record_count,
  avg(tempo) avg_tempo
FROM million_songs 
group by time_signature, artist_name, key

-- COMMAND ----------

SELECT count(1) from million_songs_delta;

-- COMMAND ----------

SELECT 
  time_signature,
  key,
  artist_name,
  count(1) record_count,
  avg(tempo) avg_tempo
FROM million_songs_delta
group by time_signature, artist_name, key

-- COMMAND ----------

-- Create schema on top of files in blob storage

DROP TABLE IF EXISTS million_songs_external;

CREATE EXTERNAL TABLE million_songs_external
(
  artist_id string,
  artist_latitude string,
  artist_longitude string,
  artist_location string,
  artist_name string,
  duration double,
  end_of_fade_in double,
  key integer,
  key_confidence double,
  loudness double,
  release string,
  song_hotness string,
  song_id string,
  start_of_fade_out double,
  tempo double,
  time_signature integer,
  time_signature_confidence double,
  title string,
  year integer,
  partial_sequence string
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
--OPTIONS ('sep'='\t', 'header'='true')
LOCATION '/databricks-datasets/songs/data-001';


-- COMMAND ----------

-- Select from external table
SELECT
  ceil(duration/60) duration_bin,
  AVG(song_hotness) as avg_hotness
  --count(1) AS record_count
FROM million_songs_external
GROUP BY ceil(duration/60)
ORDER BY duration_bin
;

-- COMMAND ----------

DROP TABLE IF EXISTS tmp_million_songs;

CREATE TEMPORARY VIEW tmp_million_songs AS Select * From million_songs where key < 4;


SELECT
  artist_name,
  AVG(tempo) as avg_tempo
FROM tmp_million_songs 
GROUP BY artist_name;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## NYC Yellow Trips examples

-- COMMAND ----------

-- Add schema on top of azure blob storage folder
DROP TABLE IF EXISTS trips_external;

CREATE EXTERNAL TABLE trips_external
(
VendorID int,
tpep_pickup_datetime timestamp,
tpep_dropoff_datetime timestamp,
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
tip_amount float,
tolls_amount float,
improvement_surcharge float,
total_amount float,
pickup_dt date,
dropoff_dt date
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1")
LOCATION "/mnt/blobdemo/nyc_taxi_raw";


-- COMMAND ----------

select * from trips_external limit 10; 

-- COMMAND ----------

-- MAGIC %fs ls /mnt/blobdemo/nyc_taxi_raw/

-- COMMAND ----------

-- MAGIC %fs ls /mnt/blobdemo/nyc_taxi/yellow_trips/

-- COMMAND ----------

-- Add schema on top of azure blob storage folder
DROP TABLE IF EXISTS trips_external;

CREATE EXTERNAL TABLE trips_external
(
VendorID int,
tpep_pickup_datetime timestamp,
tpep_dropoff_datetime timestamp,
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
tip_amount float,
tolls_amount float,
improvement_surcharge float,
total_amount float,
pickup_dt date,
dropoff_dt date
)
STORED AS PARQUET
PARTITIONED BY (year_month string)
LOCATION "/mnt/blobdemo/nyc_taxi/yellow_trips";

-- COMMAND ----------

-- -- another way to create TEMPORARY TABLE
-- DROP TABLE IF EXISTS tmp_trips;

-- CREATE TEMPORARY TABLE tmp_trips 
-- (
-- VendorID int,
-- tpep_pickup_datetime timestamp,
-- tpep_dropoff_datetime timestamp,
-- passenger_count int,
-- trip_distance float,
-- RatecodeID int,
-- store_and_fwd_flag string,
-- PULocationID int,
-- DOLocationID int,
-- payment_type int,
-- fare_amount float,
-- extra float,
-- mta_tax float,
-- tip_amount float,
-- tolls_amount float,
-- improvement_surcharge float,
-- total_amount float,
-- pickup_dt timestamp,
-- dropoff_dt timestamp
-- )
-- USING org.apache.spark.sql.parquet
-- OPTIONS (
--   path "/mnt/blobdemo/nyc_taxi/yellow_trips/year_month=2018_12"
-- );