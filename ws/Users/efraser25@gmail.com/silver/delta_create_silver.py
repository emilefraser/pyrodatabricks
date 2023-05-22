# Databricks notebook source
# MAGIC %md
# MAGIC ## Delta Table Creation scripts

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG lotto;
# MAGIC
# MAGIC -- -- Creates master entities if needed 
# MAGIC -- CREATE TABLE IF NOT EXISTS silver.master_entity (
# MAGIC --     euid string,
# MAGIC --     entity_name string,
# MAGIC --     entity_uid string,
# MAGIC --     source_uid string,
# MAGIC --     is_active boolean,
# MAGIC --     is_deleted boolean,
# MAGIC --     create_timestamp timestamp,
# MAGIC --     replicate_timestamp timestamp,
# MAGIC --     bronze_timestamp timestamp,
# MAGIC --     silver_timestamp timestamp
# MAGIC -- )
# MAGIC -- LOCATION "/mnt/silver/project=lotto/source=master_data/object=master_entity";
# MAGIC
# MAGIC
# MAGIC -- CREATE TABLE IF NOT EXISTS trips_external
# MAGIC -- LOCATION 'abfss://<bucket_path>'
# MAGIC -- AS SELECT * from samples.nyctaxi.trips;
# MAGIC  
# MAGIC -- To use a storage credential directly, add 'WITH (CREDENTIAL <credential_name>)' to the SQL statement.
# MAGIC CREATE TABLE IF NOT EXISTS silver.master_entity (
# MAGIC     euid string,
# MAGIC     entity_name string,
# MAGIC     entity_uid string,
# MAGIC     source_uid string,
# MAGIC     is_active boolean,
# MAGIC     is_deleted boolean,
# MAGIC     create_timestamp timestamp,
# MAGIC     replicate_timestamp timestamp,
# MAGIC     bronze_timestamp timestamp,
# MAGIC     silver_timestamp timestamp
# MAGIC )
# MAGIC --LOCATION 'abfss://silver/project=lotto/source=master_data/object=master_entity'
# MAGIC --OPTIONS(path '/FileStore/logs/*',header=true)

# COMMAND ----------

display(spark.catalog.listTables("hive_metastore.lotto_silver"))

# COMMAND ----------

