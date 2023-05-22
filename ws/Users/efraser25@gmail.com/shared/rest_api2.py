# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Rest API Consumer
# MAGIC
# MAGIC This serves as the generic Rest API consumer that will consume all rest api events
# MAGIC
# MAGIC Serves as a generic way to consume rest api's
# MAGIC - Performs Authentication, by getting Bearer Token
# MAGIC - Found the idea here:
# MAGIC
# MAGIC [Medium Link](https://medium.com/geekculture/how-to-execute-a-rest-api-call-on-apache-spark-the-right-way-in-python-4367f2740e78)

# COMMAND ----------

# text: Input a value in a text box.
# dropdown: Select a value from a list of provided values.
# combobox: Combination of text and dropdown. Select a value from a provided list or input one in the text box.
# multiselect: Select one or more values from a list of provided values.
dbutils.widgets.dropdown("Authentication", "None", 
                         ["None", "Bearer", "SAS Key", "UNPW"], "Choose Authentication Method")



dbutils.widgets.dropdown("authentication", "CA", ["CA", "IL", "MI", "NY", "OR", "VA"])

dbutils.widgets.text("database", "customers_dev")

# COMMAND ----------

# Imports of Libraries Needed
from pyspark.sql import SparkSession
import requests
import json
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import Row

# COMMAND ----------

# Use Single Function fo

# COMMAND ----------

# https://medium.com/geekculture/how-to-execute-a-rest-api-call-on-apache-spark-the-right-way-in-python-4367f2740e78
# Serves as a generic way to consume rest api's
# Performs Authentication, by getting Bearer Token


#
headers = {
    'content-type': "application/json"
}

body = json.dumps({
})

# Response Function
def executeRestApi(verb, url, headers, body):
  res = None
  # Make API request, get response object back, create dataframe from above schema.
  try:
    if verb == "get":
      res = requests.get(url, date=body, headers=headers)
    elif verb == "post":
      res = requests.post(url, data=body, headers=headers)
    else:
      print("another HTTP verb action")
  except Exception as e:
    return e

  if res != None and res.status_code == 200:
    return json.loads(res.text)

  return None

# To return single value for the row
# generic StringType returned to make this generic
udf_executeRestApi = udf(executeRestApi, StringType())

RestApiRequestRow = Row("verb", "url", "headers", "body")
request_df = spark.createDataFrame([
            RestApiRequestRow("get", "https://www.nationallottery.co.za/index.php?task=results.redirectPageURL&amp;Itemid=265&amp;option=com_weaver&amp;controller=lotto-history", headers, body)
          ])

result_df = request_df \
             .withColumn("result", udf_executeRestApi(col("verb"), col("url"), col("headers"), col("body")))  

#schema = F.schema_of_json(df.select('params').head()[0])

display(result_df)
#df = result_df.select(explode(col("result.videoData")).alias("results"))
#df=df.select(col("results.*"))
#display(df)
#df.select(collapse_columns(df.schema)).show()    
