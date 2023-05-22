# Databricks notebook source
# MAGIC %md
# MAGIC ## Create Schema

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS lotto_replica 
# MAGIC COMMENT 'This is the lotto_replica schema for all lotto metadata' 
# MAGIC LOCATION '/mnt/metadata/schema/lotto_replica';

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS lotto_bronze 
# MAGIC COMMENT 'This is the lotto_bronze schema for all lotto metadata' 
# MAGIC LOCATION '/mnt/metadata/schema/lotto_bronze';

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS lotto_silver
# MAGIC COMMENT 'This is the lotto_silver schema for all lotto metadata' 
# MAGIC LOCATION '/mnt/metadata/schema/lotto_silver';

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS lotto_gold
# MAGIC COMMENT 'This is the lotto_gold schema for all lotto metadata' 
# MAGIC LOCATION '/mnt/metadata/schema/lotto_gold';

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS lotto_platinum
# MAGIC COMMENT 'This is the lotto_platinum schema for all lotto metadata' 
# MAGIC LOCATION '/mnt/metadata/schema/lotto_platinum';

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC drop table `hive_metastore`.`lotto`.`master_entity`