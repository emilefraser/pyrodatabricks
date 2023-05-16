# Databricks notebook source
# Python code to mount and access Azure Data Lake Storage Gen2 Account to Azure Databricks with Service Principal and OAuth
# keyvault scope to extract secrets
keyvault_scope = "integrations_scope"

# adls variables to limit scope of mount
adls_account_name = "azstgcdatprdsan01"
adls_container_name = "databricks"
adls_folder_name = "dbc"

# keyvault secret names to extract
application_client_name = "az-adsp-int-prd-san-01-client-id"
application_client_secret = "az-adsp-int-prd-san-01-secret-value"
application_tenant_id = "az-adsp-int-prd-san-01-directory-id"

# mount point
mountPoint = "/mnt/azstgcdatprdsan01_databricks_dbc/"

# COMMAND ----------

## Gets relevant items from the keyvault
# Application (Client) ID
application_client_id = dbutils.secrets.get(scope=keyvault_scope,key=application_client_name)

# Application (Client) Secret Key
application_client_secret = dbutils.secrets.get(scope=keyvault_scope,key=application_client_secret)

# Directory (Tenant) ID
application_tenant_id = dbutils.secrets.get(scope=keyvault_scope,key=application_tenant_id)

# COMMAND ----------

for char in application_client_id:
    print(char, end="")


# COMMAND ----------

# construction of variables to use in the connection configs
endpoint = "https://login.microsoftonline.com/" + application_tenant_id + "/oauth2/token"
source = "abfss://" + adls_container_name + "@" + adls_account_name + ".dfs.core.windows.net/" + adls_folder_name

# COMMAND ----------


# Connecting using Service Principal secrets and OAuth
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": application_client_id,
           "fs.azure.account.oauth2.client.secret": application_client_secret,
           "fs.azure.account.oauth2.client.endpoint": endpoint}

# Mounting ADLS Storage to DBFS
# Mount only if the directory is not already mounted
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = source,
    mount_point = mountPoint,
    extra_configs = configs)

# COMMAND ----------

dbutils.fs.ls("mnt/azstgcdatprdsan01_databricks_dbc/")

# COMMAND ----------

# MAGIC %fs mounts

# COMMAND ----------

display(dbutils.fs.mounts()) 

# COMMAND ----------

# MAGIC %pip download --prefer-binary databricks-cli

# COMMAND ----------

# MAGIC %fs ls /

# COMMAND ----------

pip install databricks-cli

# COMMAND ----------

# MAGIC %sh
# MAGIC #!/bin/bash
# MAGIC databricks --version

# COMMAND ----------

# MAGIC %sh
# MAGIC #!/bin/bash
# MAGIC DATABRICKS_HOST="https://adb-4679147116651625.5.azuredatabricks.net"
# MAGIC DATABRICKS_TOKEN="dapi9d0b0a6dc25e151c0e76c00ec525b8e3"
# MAGIC
# MAGIC export $DATABRICKS_HOST
# MAGIC export $DATABRICKS_TOKEN

# COMMAND ----------

# MAGIC %fs ls  mnt

# COMMAND ----------

# MAGIC %fs ls dbfs:/mnt/azstgcdatprdsan01_databricks_dbc/spark/spark_api_guide/

# COMMAND ----------

# MAGIC %sh
# MAGIC #!/bin/bash
# MAGIC databricks workspace import --language SCALA --overwrite "/dbfs/mnt/azstgcdatprdsan01_databricks_dbc/spark/spark_api_guide/1sparksession.dbc" "/Users/efraser25@gmail.com/import_test.dbc"

# COMMAND ----------

# MAGIC %sh
# MAGIC #!/bin/bash
# MAGIC databricks workspace import_dir  "/dbfs/mnt/azstgcdatprdsan01_databricks_dbc/spark/spark_api_guide" "/Users/efraser25@gmail.com/import_tests"

# COMMAND ----------

# MAGIC %sh 
# MAGIC #!/bin/bash
# MAGIC
# MAGIC pwd
# MAGIC ls -la /dbfs/mnt/azstgcdatprdsan01_databricks_dbc/spark/spark_api_guide/1sparksession.dbc

# COMMAND ----------

