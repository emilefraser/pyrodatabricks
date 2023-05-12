# Databricks notebook source
# MAGIC %md
# MAGIC # other code to do http

# COMMAND ----------

import http
import json
def call_publicapi(table_name):
  """
  purpose:
    This function does bla bla bla. 
  params: reads 3 global parameters 
    status, execution_log: for sttaus and loogging
    database name: for creating database
  response:
    returns appropraite success or error message
  """
  status = ''
  execution_log = ''
  try:
    conn = http.client.HTTPSConnection("api.postcodes.io")
    payload = ''
    # headers = {
    #           'Cookie': '__cfduid=d2e270bea97599e2fbde210bf483fcd491615195032'
    #           }
    for val in range(2):
      conn.request("GET", "/random/postcodes", payload, headers)
      execution_log += 'connection is done'
      res = conn.getresponse()
      data = res.read().decode("utf-8")
      jsondata = json.loads(json.dumps(data))
      execution_log += 'JSON payload is done'
      df = spark.read.json(sc.parallelize([jsondata]))
      if val == 0:
        df_temp = df.selectExpr("string(status) as status","result['country'] as country", "result['european_electoral_region'] as european_electoral_region", "string(result['latitude']) as latitude", "string(result['longitude']) as longitude", "result['parliamentary_constituency'] as parliamentary_constituency", "result['region'] as region","'' as vld_status","'' as vld_status_reason")
        df_union = df_temp
      else:
        df_union = df_union.union(df_temp)
      df_union.write.format("delta").mode("append").saveAsTable(f"{table_name}")

    #your work
    status = 'success'
    execution_log = f"call_publicapi - success - created successfully"
  except Exception as execution_error:
    status = 'failed'
    execution_log = f"call_publicapi - failed - with error {str(execution_error)}"
  return status, execution_log


call_publicapi('uk_public_api')

# COMMAND ----------

#################################################################################################################
#
#  Oct 2022 - Since originally writing this demo, the example URL https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json
#             is terminating all requests.  The end result is that it will appear as if the code isn't work.  The problem
#             is that when the Python Requests library executes the request, the remote server terminates the request
#             and an exception is thrown.
#
#             The code is still valid, but I recommend trying with a different endpoint
#
from pyspark.sql import SparkSession
import requests
import json
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, ArrayType
from pyspark.sql import Row

#
headers = {
    'content-type': "application/json"
}

body = json.dumps({
})

# response function - udf
def executeRestApi(verb, url, headers, body):
  res = None
  # Make API request, get response object back, create dataframe from above schema.
  try:
    if verb == "get":
      res = requests.get(url, data=body, headers=headers)
    elif verb == "post":
      res = requests.post(url, data=body, headers=headers)
    else:
      print("another HTTP verb action")
  except Exception as e:
    return e

  if res != None and res.status_code == 200:
    return json.loads(res.text)

  return None

#
schema = StructType([
  StructField("Count", IntegerType(), True),
  StructField("Message", StringType(), True),
  StructField("SearchCriteria", StringType(), True),
  StructField("Results", ArrayType(
    StructType([
      StructField("Make_ID", IntegerType()),
      StructField("Make_Name", StringType())
    ])
  ))
])

#
udf_executeRestApi = udf(executeRestApi, schema)

spark = SparkSession.builder.appName("UDF REST Demo").getOrCreate()

# requests
RestApiRequest = Row("verb", "url", "headers", "body")
request_df = spark.createDataFrame([
            RestApiRequest("get", "https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json", headers, body)
          ])\
          .withColumn("execute", udf_executeRestApi(col("verb"), col("url"), col("headers"), col("body")))

request_df.select(explode(col("execute.Results")).alias("results"))\
    .select(col("results.Make_ID"), col("results.Make_Name")).show()

#spark.stop()

# COMMAND ----------

# https://medium.com/geekculture/how-to-execute-a-rest-api-call-on-apache-spark-the-right-way-in-python-4367f2740e78
#################################################################################################################
#
#  Oct 2022 - Since originally writing this demo, the example URL https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json
#             is terminating all requests.  The end result is that it will appear as if the code isn't work.  The problem
#             is that when the Python Requests library executes the request, the remote server terminates the request
#             and an exception is thrown.
#
#             The code is still valid, but I recommend trying with a different endpoint
#
from pyspark.sql import SparkSession
import requests
import json
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, ArrayType
from pyspark.sql import Row

#
headers = {
    'content-type': "application/json"
  #  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36 EdgA/90.0.818.46'
}

body = json.dumps({
})

# response function - udf
def executeRestApi(verb, url, headers, body):
  res = None
  # Make API request, get response object back, create dataframe from above schema.
  try:
    if verb == "get":
      res = requests.get(url, headers=headers)
    elif verb == "post":
      res = requests.post(url, data=body, headers=headers)
    else:
      print("another HTTP verb action")
  except Exception as e:
    return e

  if res != None and res.status_code == 200:
    return json.loads(res.text)

  return None

schema = StructType([
  StructField("Count", IntegerType(), True),
  StructField("Message", StringType(), True),
  StructField("SearchCriteria", StringType(), True),
  StructField("Results", ArrayType(
    StructType([
      StructField("Make_ID", IntegerType()),
      StructField("Make_Name", StringType())
    ])
  ))
])

def get_all_columns_from_schema(source_schema):
  branches = []
  def inner_get(schema, ancestor=None):
    if ancestor is None: ancestor = []
    for field in schema.fields:
      branch_path = ancestor+[field.name]     
      if isinstance(field.dataType, StructType):    
        inner_get(field.dataType, branch_path) 
      else:
        branches.append(branch_path)
        
  inner_get(source_schema)
        
  return branches

def collapse_columns(source_schema, columnFilter=None):
  _columns_to_select = []
  if columnFilter is None: columnFilter = ""
  _all_columns = get_all_columns_from_schema(source_schema)
  for column_collection in _all_columns:
    if (len(columnFilter) > 0) & (column_collection[0] != columnFilter): 
        continue
    # columns with questionable character choices like a space, need to be wrapped
    # in `` characters.  The alias function will do this automatically, but the selection of the column
    # e.g. col("col name") will not
    select_column_collection = ['`%s`' % list_item for list_item in column_collection]    
    
    if len(column_collection) > 1:
      _columns_to_select.append(col('.'.join(select_column_collection)).alias('_'.join(column_collection)))
    else:
      _columns_to_select.append(col(select_column_collection[0]))
  return _columns_to_select

# as above but for individual columns
def collapse_column(source_df, source_column):
    column_name = ""
    if isinstance(source_column, Column):
      column_name = source_column.name
    else:
      column_name = source_column
    return collapse_columns(source_df.schema, column_name)



# #
udf_executeRestApi = udf(executeRestApi, schema)

RestApiRequestRow = Row("verb", "url", "headers", "body")
request_df = spark.createDataFrame([
            RestApiRequestRow("get", "https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json", headers, body)
          ])

result_df = request_df \
             .withColumn("result", udf_executeRestApi(col("verb"), col("url"), col("headers"), col("body")))      

display(result_df)
#df = result_df.select(explode(col("result.Results")).alias("results"))
#display(df)
#df.select(collapse_columns(df.schema)).show()    


# COMMAND ----------

# https://medium.com/geekculture/how-to-execute-a-rest-api-call-on-apache-spark-the-right-way-in-python-4367f2740e78
#################################################################################################################
#
#  Oct 2022 - Since originally writing this demo, the example URL https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json
#             is terminating all requests.  The end result is that it will appear as if the code isn't work.  The problem
#             is that when the Python Requests library executes the request, the remote server terminates the request
#             and an exception is thrown.
#
#             The code is still valid, but I recommend trying with a different endpoint
#
from pyspark.sql import SparkSession
import requests
import json
from pyspark.sql.functions import udf, col, explode, from_json, schema_of_json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, ArrayType
from pyspark.sql import Row

#
headers = {
    'content-type': "application/json"
}

body = json.dumps({
})

# response function - udf
def executeRestApi(verb, url, headers, body):
  res = None
  # Make API request, get response object back, create dataframe from above schema.
  try:
    if verb == "get":
      res = requests.get(url, headers=headers)
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


# COMMAND ----------


url = "https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json"
headers = {
    'content-type': "application/json"
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36 EdgA/90.0.818.46'
}
res = requests.get(url, headers=headers)
json.loads(res.text)

# COMMAND ----------


url = "https://www.nationallottery.co.za/index.php?task=results.redirectPageURL&amp;Itemid=265&amp;option=com_weaver&amp;controller=lotto-history"
headers = {
    'content-type': "application/json"
}
res = requests.get(url, headers=headers)
json.loads(res.text)

# COMMAND ----------

#https://www.databricks.com/blog/2023/03/02/scalable-spark-structured-streaming-rest-api-destinations.html
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import math
import requests 
from requests.adapters import HTTPAdapter
 
def preBatchRecordsForRestCall(microBatchDf, batchSize):
    batch_count = math.ceil(microBatchDf.count() / batchSize)
    microBatchDf = microBatchDf.withColumn("content", to_json(struct(col("*"))))
    microBatchDf = microBatchDf.withColumn("row_number",\
                                            row_number().over(Window().orderBy(lit('A'))))
    microBatchDf = microBatchDf.withColumn("batch_id", col("row_number") % batch_count)
    return microBatchDf.groupBy("batch_id").\
                                          agg(concat_ws(",|", collect_list("content")).\
                                          alias("payload"))

  
def callRestAPIBatch(df, batchId):
  restapi_uri = "<REST API URL>"   
    
  @udf("string")
  def callRestApiOnce(x):
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=3)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
 
    #this code sample calls an unauthenticated REST endpoint; add headers necessary for auth    
    headers = {'Authorization':'abcd'}
    response = session.post(restapi_uri, headers=headers, data=x, verify=False)
    if not (response.status_code==200 or response.status_code==201) :
      raise Exception("Response status : {} .Response message : {}".\
                      format(str(response.status_code),response.text))
        
    return str(response.status_code)
  
  ### Call helper method to transform df to pre-batched df with one row per REST API call
  ### The POST body size and formatting is dictated by the target API; this is an example
  pre_batched_df = preBatchRecordsForRestCall(df, 10)
  
  ### Repartition pre-batched df for target parallelism of API calls
  new_df = pre_batched_df.repartition(8)
 
  ### Invoke helper method to call REST API once per row in the pre-batched df
  submitted_df = new_df.withColumn("RestAPIResponseCode",\
                                    callRestApiOnce(new_df["payload"])).collect()
 
     
dfSource = (spark.readStream
                .format("delta")
                .table("samples.nyctaxi.trips"))

streamHandle = (dfSource.writeStream
                       .foreachBatch(callRestAPIBatch)
                       .trigger(availableNow=True)
                       .start())

# COMMAND ----------

import urllib
df = spark.createDataFrame(
  [("url1", "params1"), ("url2", "params2")],
  ("url", "params"))

@udf("body string, status int")
def do_request(url: str, params: str):
  with urllib.request.urlopen(url) as f:
    status = f.status
    body = f.read().decode("utf-8")
  
  return {'status': status, 'body': body}
  

res = df.withColumn("result", do_requests(col("url"), col("params")))

# COMMAND ----------

