# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Generic REST API consumer notebook
# MAGIC This serves as the generic Rest API consumer that will consume all rest api events
# MAGIC
# MAGIC [Medium Link](https://medium.com/geekculture/how-to-execute-a-rest-api-call-on-apache-spark-the-right-way-in-python-4367f2740e78)

# COMMAND ----------

# Imports of Libraries Needed
from pyspark.sql import SparkSession
import requests
import json

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
    elif verb == "put":
        response = requests.put(url, data=body, headers=headers)
    elif verb == "patch":
        response = requests.patch(url, data=body, headers=headers)
    elif verb == "delete":
        response = requests.delete(url, data=body, headers=headers)
    else:
        return None
  except Exception as e:
    return e

  if response != None and response.status_code == 200:
    return json.loads(response.text)

  return None