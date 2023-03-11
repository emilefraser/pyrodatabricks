# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS cdc_db;
# MAGIC USE cdc_db;
# MAGIC 
# MAGIC CREATE TABLE customer (
# MAGIC   customer_id INT, 
# MAGIC   current_city STRING, 
# MAGIC   current BOOLEAN,
# MAGIC   effective_date STRING, 
# MAGIC   end_date STRING 
# MAGIC )
# MAGIC USING DELTA 
# MAGIC LOCATION '/mnt/00-mchan-demo/databricks-cookbook/cdf_table/' -- change to your own bucket path -- 
# MAGIC TBLPROPERTIES (delta.enableChangeDataFeed = true); 

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO customer
# MAGIC   SELECT 1 customer_id, "Toronto" AS current_city, true AS current, "2023-01-01" AS effective_date, NULL as end_date
# MAGIC   UNION 
# MAGIC   SELECT 2 customer_id, "Vancouver" AS current_city, true AS current, "2023-01-01" AS effective_date, NULL as end_date
# MAGIC   UNION 
# MAGIC   SELECT 3 customer_id, "Montreal" AS current_city, true AS current, "2023-01-01" AS effective_date, NULL as end_date
# MAGIC   UNION 
# MAGIC   SELECT 4 customer_id, "Calgary" AS current_city, true AS current, "2023-01-01" AS effective_date, NULL as end_date
# MAGIC   UNION 
# MAGIC   SELECT 5 customer_id, "Halifax" AS current_city, true AS current, "2023-01-01" AS effective_date, NULL as end_date;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM customer;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW updates 
# MAGIC AS 
# MAGIC SELECT 1 customer_id, "Hamilton" AS current_city, true AS current, "2023-01-02" AS effective_date, NULL as end_date
# MAGIC UNION 
# MAGIC SELECT 6 customer_id, "Burnaby" AS current_city, true AS current, "2023-01-02" AS effective_date, NULL as end_date;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM updates;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO customer AS t2
# MAGIC USING (
# MAGIC     SELECT t1.customer_id AS merge, t1.*
# MAGIC     FROM updates t1
# MAGIC     UNION ALL 
# MAGIC     SELECT NULL AS merge, t1.*
# MAGIC     FROM updates t1
# MAGIC     INNER JOIN customer t2 on t1.customer_id = t2.customer_id 
# MAGIC     WHERE t2.current = true 
# MAGIC ) t3
# MAGIC ON t2.customer_id = t3.merge
# MAGIC WHEN MATCHED AND t2.current = true THEN 
# MAGIC UPDATE SET current = false, end_date = t3.effective_date
# MAGIC WHEN NOT MATCHED THEN INSERT *

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from customer;
