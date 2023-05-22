# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Path intialization 
# MAGIC
# MAGIC Initializes file name and path for the following layers:
# MAGIC - replicate
# MAGIC - bronze
# MAGIC - silver
# MAGIC - gold
# MAGIC - platinum 
# MAGIC
# MAGIC This includes the schema paths of storage locations

# COMMAND ----------

from datetime import datetime
from enum import Enum


# COMMAND ----------

class source_target(Enum):
    undefine = 0
    source = 1
    target = 2


# COMMAND ----------

class MedallionPaths:
    def __init__(self):

        # master table storage
        self.table_storage_url_template = """https://{storage_account_name}.table.core.windows.net/{table_entity_name}()"""
        
        ## replica
        self.replica_path_template = """/mnt/replica/project={project_name}/source={source_name}/object={object_name}/year={now.strftime("%Y")}/month={now.strftime("%m")}/day={now.strftime("%d")}/hour={now.strftime("%H")}/minute={now.strftime("%M")}/second={now.strftime("%S")}/"""
        self.replica_path_timepart_template = """/mnt/replica/project={project_name}/source={source_name}/object={object_name}/"""
        self.replica_file_name_template = """{object_name}_{now.strftime("%Y")}{now.strftime("%m")}{now.strftime("%d")}_{now.strftime("%H")}{now.strftime("%M")}{now.strftime("%S")}.{file_format}"""
        self.replica_file_format = """{file_format}"""

        # bronze (delta format)
        self.bronze_path_template = """/mnt/bronze/project={project_name}/source={source_name}/object={object_name}/"""
        self.bronze_file_format = "delta"

        # silver 
        self.silver_path_template = """/mnt/silver/project={project_name}/source={source_name}/object={object_name}/"""
        self.slver_file_format = "delta"

        #gold
        self.gold_path_template = """/mnt/gold/entity={entity_name}/"""
        self.gold_file_format = "delta"



    # getter methods for all the paths available 
    # replica
    def get_table_storage_url(self, storage_account_name, table_entity_name):
        return self.get_path_value(self.table_storage_url_template)

    def get_replica_path(self, project_name, source_name, object_name, now): 
        return self.get_path_value(self.replica_path_template)

    def get_replica_path_without_timepart(self, project_name, source_name, object_name): 
        return self.get_path_value(self.replica_path_timepart_template)

    def get_replica_file_name(self, object_name, file_format, now): 
        return self.get_path_value(self.replica_file_name_template)

    def get_replica_file_path(self, project_name, source_name, object_name, file_format, now): 
        return self.get_path_value(self.get_replica_path(project_name, source_name, object_name, now) + self.get_replica_file_name(object_name, file_format, now))

    def get_replica_file_format(self, file_format): 
        return self.get_path_value(self.replica_file_format_template)

    def get_bronze_path(self, project_name, source_name, object_name): 
        return self.get_path_value(self.bronze_path_template)

    def get_bronze_schema_location_path(self, project_name, source_name, object_name): 
        return self.get_path_value(self.bronze_path_template) 

    def get_bronze_checkpoint_location_path(self, project_name, source_name, object_name): 
        return self.get_path_value(self.bronze_path_template) + "/_checkpoint"
    
    def get_bronze_file_format(self): 
        return self.bronze_file_format

    # silver
    def get_silver_path(self, project_name, source_name, object_name): 
        return self.get_path_value(self.silver_path_template)

    def get_silver_checkpoint_location_path(self, project_name, source_name, object_name): 
        return self.get_path_value(self.silver_path_template) + "/_checkpoint"
    
    def get_silver_file_format(self): 
        return self.silver_file_format

    def get_gold_path(self, entity_name): 
        return self.get_path_value(self.gold_path_template)

    def get_gold_file_format(self): 
        return self.gold_file_format

    # dynamic f string expander
    def get_path_value(self, template):
        return eval(f"f'{template}'")