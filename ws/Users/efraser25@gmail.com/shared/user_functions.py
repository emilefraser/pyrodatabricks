# Databricks notebook source
# MAGIC %md
# MAGIC ## User Functions
# MAGIC
# MAGIC Global User Defined Functions for the population of the data. Will include:
# MAGIC - Merges
# MAGIC - Generic code

# COMMAND ----------

# generic upsert from source to target
# only Insert/Update
# target needs to be defined already and be called target_delta
def upsert_to_delta(source_df, batchId):
  target_delta.alias("target").merge(
      source_df.alias("source"),
      "source.euid = target.euid") \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .execute()

# COMMAND ----------

# generic upsert from source to target
# only Insert/Update
# target needs to be defined already and be called target_delta
def merge_to_delta(source_df, batchId):
  target_delta.alias("target").merge(
      source_df.alias("source"),
      "source.euid = target.euid") \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .whenNotMatchedBySourceDelete() \
    .execute()