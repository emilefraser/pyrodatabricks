# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Master Data Azure Table Storage API Consumer
# MAGIC
# MAGIC This serves as the generic Rest API consumer that will consume all rest api events
# MAGIC
# MAGIC Does the init to connect to table storage
# MAGIC
# MAGIC [Medium Link](https://medium.com/geekculture/how-to-execute-a-rest-api-call-on-apache-spark-the-right-way-in-python-4367f2740e78)

# COMMAND ----------

# Imports of Libraries Needed
from pyspark.sql import SparkSession
import requests
import json
from pyspark.sql.functions import udf, col, explode

# COMMAND ----------

# Gets necessary data from the key vault back secret scope
application_id = dbutils.secrets.get("integrations_scope", "az-adsp-dbr-int-prd-san-01-clientid")
application_secret = dbutils.secrets.get("integrations_scope", "az-adsp-dbr-int-prd-san-01-clientsecret")
tenant_id = dbutils.secrets.get("integrations_scope", "tenant-id")

# COMMAND ----------

# Use Single Function to do authentiction (with Bearer Token)
def executeRestApi(verb, url, headers, body):
  response = None
  # Make API request, get response object back, create dataframe from above schema.
  try:
    if verb == "post":
        response = requests.post(url, data=body, headers=headers)
    elif verb == "get":
        response = requests.get(url, data=body, headers=headers)
    else:
        return None
  except Exception as e:
    return e

  if response != None and response.status_code == 200:
    return json.loads(response.text)

  return None

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
display(token)

# COMMAND ----------

# gets all the master entities from the entities table
verb = "get"
table_storage_account="azstg2datstgprdsan01"
url = f"https://{table_storage_account}.table.core.windows.net/entities()"
headers = {
    "Authorization": token,
    "Accept": "application/json",
    "x-ms-version": "2020-08-04"
}

body = { 
}
# write this out as json to dls
response = executeRestApi(verb, url, headers, body)
display(response["value"])


