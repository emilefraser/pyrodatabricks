# Databricks notebook source
## Initialize Untity Catalog 

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS lotto;
# MAGIC COMMENT 'Creates lotto catalog';

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG lotto;
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS source
# MAGIC -- MANAGED LOCATION '<location_path>']
# MAGIC COMMENT 'Creates source schema on the lotto catalog';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS replica
# MAGIC -- MANAGED LOCATION '<location_path>']
# MAGIC COMMENT 'Creates replica schema on the lotto catalog';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS bronze
# MAGIC -- MANAGED LOCATION '<location_path>' ]
# MAGIC COMMENT 'Creates bronze schema on the lotto catalog';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS silver
# MAGIC -- MANAGED LOCATION '<location_path>' ]
# MAGIC COMMENT 'Creates silver schema on the lotto catalog';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS gold
# MAGIC -- MANAGED LOCATION '<location_path>' ]
# MAGIC COMMENT 'Creates gold schema on the lotto catalog';
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS  platinum
# MAGIC -- MANAGED LOCATION '<location_path>' ]
# MAGIC COMMENT 'Creates platinum schema on the lotto catalog';

# COMMAND ----------

# MAGIC %sql 
# MAGIC
# MAGIC SHOW CATALOGS;
# MAGIC SHOW SCHEMAS;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT 1

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC --1. Set the current schema
# MAGIC  USE CATALOG lotto;
# MAGIC
# MAGIC  
# MAGIC --2. create a table in the schema
# MAGIC CREATE TABLE IF NOT EXISTS replica.quickstart_table
# MAGIC (columnA Int, columnB String) PARTITIONED BY (columnA);
# MAGIC  
# MAGIC --3. Create a managed Delta table and insert two records
# MAGIC --CREATE TABLE IF NOT EXISTS quickstart_table
# MAGIC --(columnA Int, columnB String) PARTITIONED BY (columnA);
# MAGIC  
# MAGIC -- INSERT INTO TABLE replica.quickstart_table
# MAGIC -- VALUES
# MAGIC --   (1, "one"),
# MAGIC --   (2, "two");
# MAGIC  
# MAGIC
# MAGIC -- SELECT * FROM replica.quickstart_table;
# MAGIC
# MAGIC drop table replica.quickstart_table

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC select current_schema(), current_catalog(), current_database(), current_metastore()

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS quickstart_catalog;
# MAGIC  