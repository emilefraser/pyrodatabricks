# Databricks notebook source
# MAGIC %md
# MAGIC ## ![Delta Lake Tiny Logo](https://pages.databricks.com/rs/094-YMS-629/images/delta-lake-tiny-logo.png) Delta Lake
# MAGIC This notebook contains a few examples of Delta Lake created by Dustin Vannoy.  For more examples you can check out one provided by Databricks at https://dbricks.co/dlw-01

# COMMAND ----------

# MAGIC %md
# MAGIC ## Initial Setup and Read of Delta Lake tables
# MAGIC Read in a public databricks dataset and display data

# COMMAND ----------

# MAGIC %fs ls /databricks-datasets/songs/data-001/

# COMMAND ----------

from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

file_location = "/databricks-datasets/songs/data-001/part-*"

schema = StructType([
  StructField("artist_id", StringType(), False),
  StructField("artist_latitude", StringType(), False),
  StructField("artist_longitude", StringType(), False),
  StructField("artist_location", StringType(), False),
  StructField("artist_name", StringType(), False),
  StructField("duration", DoubleType(), False),
  StructField("end_of_fade_in", DoubleType(), False),
  StructField("key", IntegerType(), False),
  StructField("key_confidence", DoubleType(), False),
  StructField("loudness", DoubleType(), False),
  StructField("release", StringType(), False),
  StructField("song_hotness", StringType(), False),
  StructField("song_id",StringType(), True),
  StructField("start_of_fade_out", DoubleType(), False),
  StructField("tempo", DoubleType(), False),
  StructField("time_signature", IntegerType(), False),
  StructField("time_signature_confidence", DoubleType(), False),
  StructField("title", StringType(), False),
  StructField("year", IntegerType(), False),
  StructField("partial_sequence", StringType(), False)
  ])


# COMMAND ----------

# MAGIC %md
# MAGIC ## Cleanup scripts

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE delta_songs

# COMMAND ----------

# MAGIC %fs ls /Filestore/data/delta_demo

# COMMAND ----------

# MAGIC %fs rm -r /Filestore/data/delta_demo/songs

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Create table, loading incrementally
# MAGIC
# MAGIC For demo purposes let's load from our dataframe into a table bit by bit

# COMMAND ----------

from pyspark.sql.functions import col
song_df = spark.read.option('sep','\t').option("inferSchema", "true").csv(file_location, schema)

print(song_df.count())
display(song_df)

# COMMAND ----------

# MAGIC %md
# MAGIC Add first set of songs - everything before year 2000 (including those with year = 0)

# COMMAND ----------

destination_location = "/Filestore/data/delta_demo/delta_songs"

songs_pre2000 = song_df.filter(col("year") < 2000)
songs_pre2000.write.format("delta").mode("append").option("path", destination_location).saveAsTable("delta_songs")

# COMMAND ----------

# MAGIC %md
# MAGIC Run simple query to view our results

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC   year,
# MAGIC   COUNT(song_id) as song_count
# MAGIC FROM delta_songs 
# MAGIC GROUP BY year
# MAGIC ORDER BY year

# COMMAND ----------

# MAGIC %md
# MAGIC Let's look at the transaction history

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_songs;

# COMMAND ----------

# MAGIC %md
# MAGIC Add second set of songs - everything from year 2000 - 2005

# COMMAND ----------

# Add second set of songs - everything from year 2000 - 2005
songs_2000_2005 = song_df.filter(col("year").between(2000, 2005))
songs_2000_2005.write.format("delta").mode("append").option("path", destination_location).saveAsTable("delta_songs")

# COMMAND ----------

# MAGIC %md
# MAGIC Once more - but let's add an extra column - everything from year 2006 forward

# COMMAND ----------

from pyspark.sql.functions import ceil

songs_since_2006 = song_df.filter(col("year") >= 2006 )

# Add column
songs_since_2006 = songs_since_2006.withColumn("duration_bin", ceil(col("duration")/60))

# Drop column
songs_since_2006 = songs_since_2006.drop("artist_name")

songs_since_2006.write.format("delta").mode("append").option("path", destination_location).saveAsTable("delta_songs")

# COMMAND ----------

# MAGIC %md
# MAGIC Let's add the schema merge option to make it work.  NOTE: This leave historical entries for the new column null.

# COMMAND ----------

songs_since_2006.write.format("delta").option("mergeSchema","true").mode("append").option("path", destination_location).saveAsTable("delta_songs")

sample_results = sql("SELECT * FROM delta_songs where year = 2006")
display(sample_results)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Time Travel - Data Versioning
# MAGIC An exciting feature of Delta Lake is ability to look back at previous versions of the data.  If you have been working with big data for a while you know that this can be a challenge to pull off and usually involves extra design and development work.  With Delta Lake it's built in.
# MAGIC
# MAGIC Options:
# MAGIC 1. Using a timestamp
# MAGIC 2. Using a version number

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_songs;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- current version
# MAGIC SELECT count(*) FROM delta_songs;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- previous version
# MAGIC SELECT count(*) FROM delta_songs VERSION AS OF 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- as of previous timestamp
# MAGIC SELECT count(*) FROM delta_songs TIMESTAMP AS OF "2019-11-19 20:24:12";

# COMMAND ----------

# MAGIC %md
# MAGIC ## DeltaLog

# COMMAND ----------

# MAGIC %fs ls /Filestore/data/delta_demo/delta_songs

# COMMAND ----------

# MAGIC %fs head /Filestore/data/delta_demo/delta_songs/_delta_log/00000000000000000001.crc

# COMMAND ----------

# MAGIC %fs head /Filestore/data/delta_demo/delta_songs/_delta_log/00000000000000000001.json

# COMMAND ----------

# MAGIC %md
# MAGIC ## Update
# MAGIC We can now update values with syntax we get in a relational database

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC UPDATE delta_songs SET artist_name = 'Artist Formerly Known As Prince' WHERE artist_name = 'Prince'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Merge
# MAGIC 1. Identify rows to insert or update
# MAGIC 2. Use MERGE

# COMMAND ----------

parquet_file = "/Filestore/data/parquet_demo/songs"
tmp_df = spark.read.parquet(parquet_file)
tmp_df = tmp_df.withColumn("duration_bin", ceil(col("duration")/60))
tmp_df.createOrReplaceTempView("stage_parquet_songs")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- You need something unique to join on
# MAGIC
# MAGIC MERGE INTO delta_songs as d
# MAGIC USING stage_parquet_songs as m
# MAGIC on d.song_id = m.song_id
# MAGIC WHEN MATCHED THEN 
# MAGIC   UPDATE SET *
# MAGIC WHEN NOT MATCHED 
# MAGIC   THEN INSERT *

# COMMAND ----------

# MAGIC %md
# MAGIC ## DELETE
# MAGIC WTF...Delete in a Data Lake? Are you serious?
# MAGIC
# MAGIC yes, I am

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC DELETE FROM delta_songs WHERE year = 0

# COMMAND ----------

# MAGIC %md
# MAGIC ### But can't we do that in Parquet?
# MAGIC Glady you asked...

# COMMAND ----------

tmp_df = spark.read.parquet(parquet_file)
tmp_df.createOrReplaceTempView("tmp_parquet_songs")

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM tmp_parquet_songs where year = 0

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE tmp_parquet_songs SET artist_name = 'Artist Formerly Known As Prince' WHERE artist_name = 'Prince'

# COMMAND ----------

# MAGIC %md
# MAGIC ## Optimize and Vacuum

# COMMAND ----------

# MAGIC %fs ls /mnt/adlsdemo/delta_demo/delta_songs/

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE delta_songs ZORDER BY (year, song_id)

# COMMAND ----------

# MAGIC %sql
# MAGIC VACUUM delta_songs RETAIN 0 HOURS

# COMMAND ----------

# MAGIC %sql
# MAGIC set spark.databricks.delta.retentionDurationCheck.enabled = false;
# MAGIC VACUUM delta_songs RETAIN 0 HOURS

# COMMAND ----------

