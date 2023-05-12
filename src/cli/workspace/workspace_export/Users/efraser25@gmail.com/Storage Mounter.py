# Databricks notebook source
# MAGIC %md ### DBFS mount points
# MAGIC
# MAGIC Prerequisites:
# MAGIC - Create a Service Principal (SP) and get credentials;  application_id `<aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee>` and application_secret `<NzQzY2QzYTAtM2I3Zi00NzFmLWI3MGMtMzc4MzRjZmk=>` [Link](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal). 
# MAGIC - Get tenant_id`<ffffffff-gggg-hhhh-iiii-jjjjjjjjjjjj>` [Link](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal#get-tenant-id). 
# MAGIC - Give SP Data Blob (Reader/Contributor) rights to the storage account
# MAGIC - Create KeyVault and obtain its unique id `<aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee>`
# MAGIC - Create Secrets in KeyVault for the SP's application_id & application_secret
# MAGIC - Get databricks_instance_id through Azure or checking URL of workspace `https://<databricks_instance_id>.azuredatabricks.net/`
# MAGIC - Create a secret scope via url [ https://databricks-instance#secrets/createScope](https://<databricks-instance>#secrets/createScope) or dbutils using KeyVault Unique Id. The Databricks Resource Id is `2ff814a6-3304-4ab8-85cb-cd0e6f879c1d`
# MAGIC - Ensure scope is created with this command `dbutils.secrets.listScopes()`
# MAGIC
# MAGIC More info: [DBFS](https://docs.azuredatabricks.net/user-guide/dbfs-databricks-file-system.html)

# COMMAND ----------

# Gets necessary data from the key vault back secret scope
application_id = dbutils.secrets.get("integrations_scope", "az-adsp-dbr-int-prd-san-01-clientid")
application_secret = dbutils.secrets.get("integrations_scope", "az-adsp-dbr-int-prd-san-01-clientsecret")
tenant_id = dbutils.secrets.get("integrations_scope", "tenant-id")

# COMMAND ----------

 # Define the variables used for creating connection strings
 # #value# indicates a template which will be replaced upstream
adls_account_name = "azstg2datstgprdsan01"
adls_containers = ["source", "replica", "bronze", "silver", "gold", "repo"]
adls_folder_name = ""
dbfs_mount_point_template = "/mnt/#adls_container_name#"

# COMMAND ----------

# Set the connection configs
endpoint = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"

# Connecting using Service Principal secrets and OAuth
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": application_id,
           "fs.azure.account.oauth2.client.secret": application_secret,
           "fs.azure.account.oauth2.client.endpoint": endpoint}

# COMMAND ----------

 # Mount all unmounted containers after resolving source and mount point name
 # Only mount unmounted containers
print(f"Mounting the following containers:{adls_containers}")

for adls_container_name in adls_containers:
  source = "abfss://" + adls_container_name + "@" + adls_account_name + ".dfs.core.windows.net/" + adls_folder_name
  mount_point = dbfs_mount_point_template.replace("#adls_container_name#", adls_container_name)
 
  # Mount ADLS Storage to DBFS only if the directory is not already mounted
  if not any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts()):
    dbutils.fs.mount(
      source = source,
      mount_point = mount_point,
      extra_configs = configs)

# COMMAND ----------

# test if all containers mounted successfully
failures = 0
for adls_container in adls_containers:
  try:
    dbutils.fs.ls(f"/mnt/{adls_container}")
  except Exception as e:  
    if 'java.io.FileNotFoundException' in str(e):
      failures += 1
    else:
      raise

if failures == 0:
  print("All containers mounted successfully")
elif failures ==1:
    print(f"There is {failures} unmounted containers")
else:
  print(f"There are {failures} unmounted containers")

# COMMAND ----------

print("Storage Mounter Complete")