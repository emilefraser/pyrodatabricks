# Databricks notebook source
# MAGIC %md
# MAGIC ## Silver Schemas
# MAGIC
# MAGIC These schemas will be applied in the silver layer of transformation

# COMMAND ----------

from pyspark.sql.types import *

# COMMAND ----------

class SilverSchema:
    def __init__(self):
        self.silver_schemas = {}

    def set_schema(self, object_name, object_schema):
        self.silver_schemas[object_name] = object_schema

    def get_schema(self, object_name):
        return self.silver_schemas[object_name]

# COMMAND ----------

# sets the first schema
silver = SilverSchema()
schema_definition = StructType([ StructField("entity_uid", StringType(), True), 
                                 StructField("year", IntegerType(), True),
                                 StructField("month", IntegerType(), True),
                                 StructField("day", IntegerType(), True),
                                 StructField("_rescue_data", StringType(), False),
                                 StructField("partition_key", StringType(), True),
                                 StructField("object_id", StringType(), True),
                                 StructField("timestamp", IntegerType(), True),
                                 StructField("entity_name", StringType(), True),    
                                 StructField("odata_etag", StringType(), False),    
                                
                    ])
#print(schema_definition)
silver.set_schema('master_objects', schema_definition)
#bronze.get_schema("master_objects")

# COMMAND ----------

