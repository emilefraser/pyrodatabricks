# Databricks notebook source
# MAGIC %md
# MAGIC ## master precursor silver
# MAGIC
# MAGIC Populates the master entity list
# MAGIC
# MAGIC This notebook is used to populate and the master_entities to enable extraction of other entities

# COMMAND ----------

# MAGIC %run "../shared/initialize_paths"

# COMMAND ----------

# MAGIC %run "../shared/user_functions"

# COMMAND ----------

# Imports for the notebook
from pyspark.sql.types import *
from pyspark.sql.functions import lit
from delta.tables import *

# COMMAND ----------

## Layer variables
project_name = "lotto"
source_name = "master_data"
file_format="delta"

# For the precursor load, just need to load the objects entity
object_name = "objects"
#target_object_name = "master_entity"

# gets the target delta table to be merged into
mpath = MedallionPaths()
object_name = "objects"
source_path = mpath.get_bronze_path(project_name, source_name, object_name)
object_name = "master_entity"
target_delta_table = DeltaTable.forPath(spark, mpath.get_silver_path(project_name, source_name, object_name))
target_checkpoint_location = mpath.get_silver_checkpoint_location_path(project_name, source_name, object_name)


# COMMAND ----------



# gets the target delta table to be merged into
#target_delta = DeltaTable.forPath(spark, f"/mnt/{target_layer}/project={project_name}/source={source_name}/object={target_object_name}")

# starts the stream
source_df = (spark.readStream \
    .format("delta") \    
    .load(source_path))

## cast an rename all columns
source_df = source_df.select(
        source_df.value__RowKey.cast(StringType()).alias("euid"),
        source_df.value__entity_name.cast(StringType()).alias("entity_name"),
        source_df.odata_metadata.cast(StringType()).alias("source_uid"),
        source_df.value__is_active.cast(BooleanType()).alias("is_active"),
        source_df.value__is_deleted.cast(BooleanType()).alias("is_deleted"),
        source_df.value__Timestamp.cast(TimestampType()).alias("create_timestamp"), 
        source_df.value__Timestamp.cast(TimestampType()).alias("replicate_timestamp"), 
        source_df.value__Timestamp.cast(TimestampType()).alias("bronze_timestamp"), 
    )

## add the additional columns needed
source_df.withColumn("silver_timestamp", datetime.now())
    .withColumn("entity_uid", lit("null"))

## write the steam data to silver
query = (source_df.writeStream
    .format("delta")
    .foreachBatch(upsert_to_delta)
    .outputMode("update")
    .option("checkpointLocation", target_checkpoint_location)
    .trigger(once=True)
    .start(target_delta_table)
)

query.awaitTermination()

# COMMAND ----------

obj_path = "/mnt/silver/project=lotto/source=master_data/object=objects/"
display(spark.read.load(target_delta_table))