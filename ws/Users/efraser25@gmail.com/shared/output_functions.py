# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## General output functions 
# MAGIC
# MAGIC This contains output functions, with the following mediums being in scope:
# MAGIC - Screen
# MAGIC - File (csv, json, xml)
# MAGIC - Terminal

# COMMAND ----------

# Imports of Libraries Needed
from pyspark.sql import SparkSession
import requests
import json

# COMMAND ----------

# writes dataframe containing json to single file without partitioning info
def write_df_to_json_file(df, target_path, target_file_name):
    try:      
        (
        df.coalesce(1)
            .write
            .mode("overwrite")
            .json(f"{target_path}partition")
        )

        # moves actual data file and deletes partitioning files
        target_file_path = f"{target_path}{target_file_name}"
        files_partition= dbutils.fs.ls(f"{target_path}partition")
        replicated_file = [ i for i in files_partition if i.path.endswith(".json") ]
        dbutils.fs.cp(replicated_file[0].path, target_file_path)
        dbutils.fs.rm(f"{target_path}partition", recurse=True)
     
        return target_file_path

    except Exception as e:
        print("Could not write unpartitioned json file to the specified path:", e)
        return None
    