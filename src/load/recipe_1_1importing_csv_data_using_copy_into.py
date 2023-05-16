# Databricks notebook source
# DBTITLE 1,Create the Delta table 
# MAGIC  %sql  
# MAGIC  CREATE TABLE t1_bronze_pos_sales;

# COMMAND ----------

# DBTITLE 1,Configure COPY INTO 
# MAGIC %sql
# MAGIC COPY INTO t1_bronze_pos_sales
# MAGIC FROM 's3://databricks-cookbook/ch01_r01/' -- replace with your Cloud Storage path -- 
# MAGIC FILEFORMAT = CSV
# MAGIC VALIDATE
# MAGIC FORMAT_OPTIONS ('header' = 'true', 
# MAGIC                 'inferSchema' = 'true', 
# MAGIC                 'mergeSchema' = 'true')
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true')
