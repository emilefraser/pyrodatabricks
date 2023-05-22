# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Replicate the master data precursor
# MAGIC
# MAGIC Gets table storage entity which holds data regarding other table storage entities

# COMMAND ----------

# MAGIC %run "../shared/initialize_paths"

# COMMAND ----------

# MAGIC %run "../shared/rest_api"

# COMMAND ----------

# MAGIC %run "../shared/output_functions"

# COMMAND ----------

# local imports
from datetime import datetime

# COMMAND ----------

# Gets necessary data from the key vault back secret scope
application_id = dbutils.secrets.get("integrations_scope", "az-adsp-dbr-int-prd-san-01-clientid")
application_secret = dbutils.secrets.get("integrations_scope", "az-adsp-dbr-int-prd-san-01-clientsecret")
tenant_id = dbutils.secrets.get("integrations_scope", "tenant-id")

# COMMAND ----------

# Defines the rest of the values needed 
# Obtain bearer token to access master data with
verb = "post"
url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
headers = {
    "content-type": "application/x-www-form-urlencoded"
}

body = { 
    "grant_type": "client_credentials",
    "client_id": application_id,
    "client_secret": application_secret,
    "resource": "https://storage.azure.com/"
}

response = executeRestApi(verb, url, headers, body)
token = response["token_type"] + ' ' + response["access_token"]
#display(token)

# COMMAND ----------

# gets all the master entities from the entities 
# this one is only for objects entity
# layer info
now = datetime.now()

# api call to make
verb = "get"

# storage account to call
storage_account_name="azstg2datstgprdsan01"
table_entity_name = "objects"

project_name="lotto"
source_name="master_data"
object_name="objects"
file_format="json"

# instantize the path class
mpath = MedallionPaths()
url = mpath.get_table_storage_url(storage_account_name, table_entity_name)
target_path = mpath.get_replica_path(project_name, source_name, object_name, now)
target_file_name = mpath.get_replica_file_name(object_name, file_format, now)
target_path_without_filepath = mpath.get_replica_path_without_timepart(project_name, source_name, object_name)

#file_name = f"{object_name}_{now.strftime('%Y')}{now.strftime('%m')}{now.strftime('%d')}_{now.strftime('%H')}{now.strftime('%M')}{now.strftime('%S')}.json"

headers = {
    "Authorization": token,
    "Accept": "application/json",
    "x-ms-version": "2020-08-04"
}

body = {}

# write this out as json to dls
response = executeRestApi(verb, url, headers, body)
df = spark.read.option("multiline", "true").json(sc.parallelize([json.dumps(response)]))

# delete currently replicated master data and repopulate just before writing the file to target
dbutils.fs.rm(target_path_without_filepath ,True)

# writes the json response as single file in replicate layer
write_df_to_json_file(df, target_path, target_file_name)