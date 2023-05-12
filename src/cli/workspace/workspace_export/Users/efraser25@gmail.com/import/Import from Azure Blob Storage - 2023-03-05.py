# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC This notebook shows you how to create and query a table or DataFrame loaded from data stored in Azure Blob storage.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Step 1: Set the data location and type
# MAGIC
# MAGIC There are two ways to access Azure Blob storage: account keys and shared access signatures (SAS).
# MAGIC
# MAGIC To get started, we need to set the location and type of the file.

# COMMAND ----------

storage_account_name = "azstgcdatprdsan01"
storage_account_access_key = "0WKhqOcm/7FQIIOQSgT4r3gOKMv6MTZmX/iZOBq0907r98JQYWPAL25+H7o41yxN63yByVh3GdkN+AStsaQAVQ=="
application_id = "e643d70b-8281-4367-b181-5c123b0a2402"


# COMMAND ----------

location = "wasbs://azstgcdatprdsan01.blob.core.windows.net/databricks/notebooks/"
file_type = "dbc"
moutn_point = "/mnt/notebooks/dbc"

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": "<application-id>",
          "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope="<scope-name>",key="<service-credential-key-name>"),
          "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/<directory-id>/oauth2/token"}

# COMMAND ----------

dbutils.fs.mount(
  source = location,
  mount_point = mount_point,
)

# COMMAND ----------

spark.conf.set(
  "fs.azure.account.key."+storage_account_name+".blob.core.windows.net",
  storage_account_access_key)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Step 2: Read the data
# MAGIC
# MAGIC Now that we have specified our file metadata, we can create a DataFrame. Notice that we use an *option* to specify that we want to infer the schema from the file. We can also explicitly set this to a particular schema if we have one already.
# MAGIC
# MAGIC First, let's create a DataFrame in Python.

# COMMAND ----------

df = spark.read.format(file_type).option("inferSchema", "true").load(file_location)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Step 3: Query the data
# MAGIC
# MAGIC Now that we have created our DataFrame, we can query it. For instance, you can identify particular columns to select and display.

# COMMAND ----------

display(df.select("EXAMPLE_COLUMN"))

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Step 4: (Optional) Create a view or table
# MAGIC
# MAGIC If you want to query this data as a table, you can simply register it as a *view* or a table.

# COMMAND ----------

df.createOrReplaceTempView("YOUR_TEMP_VIEW_NAME")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC We can query this view using Spark SQL. For instance, we can perform a simple aggregation. Notice how we can use `%sql` to query the view from SQL.

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT EXAMPLE_GROUP, SUM(EXAMPLE_AGG) FROM YOUR_TEMP_VIEW_NAME GROUP BY EXAMPLE_GROUP

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Since this table is registered as a temp view, it will be available only to this notebook. If you'd like other users to be able to query this table, you can also create a table from the DataFrame.

# COMMAND ----------

df.write.format("parquet").saveAsTable("MY_PERMANENT_TABLE_NAME")

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC This table will persist across cluster restarts and allow various users across different notebooks to query this data.