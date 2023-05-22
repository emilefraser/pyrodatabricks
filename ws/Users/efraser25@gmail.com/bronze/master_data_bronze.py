# Databricks notebook source
# MAGIC %md
# MAGIC ## master data bronze

# COMMAND ----------

# MAGIC %run "../shared/initialize_paths"

# COMMAND ----------

# MAGIC %run "./structural_functions"

# COMMAND ----------

from datetime import datetime
from pyspark.sql.functions import *

# COMMAND ----------

## layer variables
project_name = "lotto"
source_name = "master_data"
object_name = "objects"
file_format="json"

# instantize the path class
mpath = MedallionPaths()
source_path = mpath.get_replica_path_without_timepart(project_name, source_name, object_name)
target_path = mpath.get_bronze_path(project_name, source_name, object_name)
target_checkpoint_location_path = mpath.get_bronze_checkpoint_location_path(project_name, source_name, object_name)
target_schema_location_path = mpath.get_bronze_schema_location_path(project_name, source_name, object_name)

# removes current bronze layer
dbutils.fs.rm(target_path ,True)

# COMMAND ----------

# AUTOLOADER READ 
source_options = {
    "cloudFiles.format": "json",
    "cloudFiles.schemaLocation": target_schema_location_path,
    "cloudFiles.schemaEvolutionMode": "rescue",
    "cloudFiles.inferColumnTypes": "true",
    "cloudFiles.allowOverwrites": "true",
    "cloudFiles.includeExistingFiles": "true",
    "cloudFiles.validateOptions": "true"
}

# reads the objects and will then loop through rest of the entitites
df = flatten_json(
        (spark.readStream.format("cloudFiles")
                    .options(**source_options)
                    .load(source_path)
        )
    )

# COMMAND ----------

# Add additional metadata columns columns
now = datetime.now()
#print(now)

# create replication timestamp
df = df.withColumn("replicate_timestamp", concat(col("year"),lit("-"),format_string("%02d", col("month")),lit("-"),format_string("%02d",col("day")),lit(" "),format_string("%02d",col("hour")),lit(":"),format_string("%02d",col("minute")),lit(":"),format_string("%02d",col("second")))).withColumn("bronze_timestamp", date_format(lit(now), "yyyy-MM-dd HH:mm:SS"))


# COMMAND ----------

# delete currently replicated master data and repopulate just before writing the file to target
dbutils.fs.rm(target_path ,True)

# COMMAND ----------

query = (df.writeStream.format("delta") \
            .option("mergeSchema", "true") \
            .option("checkpointLocation", target_schema_location_path) \
            .trigger(once=True) \
            .start(target_path))

query.awaitTermination()

# COMMAND ----------

# df = df = spark.read.format("delta").load("/mnt/bronze/project=lotto/source=master_data/object=objects/")
# display(df)
obj_path = "/mnt/bronze/project=lotto/source=master_data/object=objects/"
display(spark.read.load(obj_path))