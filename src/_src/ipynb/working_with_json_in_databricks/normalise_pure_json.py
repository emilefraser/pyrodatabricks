# Databricks notebook source
def mount_lake_container(pAdlsContainerName, pSecretScopeName, pStorageAccountName, pSecretClientID, pSecretClientSecret, pSecretTenantID):
    """
    mount_lake_container: 
        Takes a container name and mounts it to Databricks for easy access. 
        Prints out the name of the mount point. 
        Uses a service princple to authenticate.
    :param pSecretScopeName: Name of the Secret Scope set in Databricks.
    :param pStorageAccountName: Name of the generic key vault secret containing the storage account's name.
    :param pSecretClientID: Name of the generic key vault secret containing the Service Principle Name.
    :param pSecretClientSecret: Name of the generic key vault secret containing the Service Principle Password.
    :param pSecretTenantID: Name of the generic key vault secret containing the Tenent ID.
    """

    # Define the variables used for creating connection strings - Data Lake Related
    vAdlsAccountName = dbutils.secrets.get(scope=pSecretScopeName, key=pStorageAccountName)
    vMountPoint = "/mnt/datalake_" + pAdlsContainerName #fixed since we already parameterised the container name. Ensures there is a standard in mount point naming
    
    # Get the actual secrets from key vault for the service principle
    vApplicationId = dbutils.secrets.get(scope=pSecretScopeName, key=pSecretClientID) # Application (Client) ID
    vAuthenticationKey = dbutils.secrets.get(scope=pSecretScopeName, key=pSecretClientSecret) # Application (Client) Secret Key
    vTenantId = dbutils.secrets.get(scope=pSecretScopeName, key=pSecretTenantID) # Directory (Tenant) ID

    # Using the secrets above, generate the URL to the storage account and the authentication endpoint for OAuth
    vEndpoint = "https://login.microsoftonline.com/" + vTenantId + "/oauth2/token" #Fixed URL for the endpoint
    vSource = "abfss://" + pAdlsContainerName + "@" + vAdlsAccountName + ".dfs.core.windows.net/"

    # Connecting using Service Principal secrets and OAuth
    vConfigs = {"fs.azure.account.auth.type": "OAuth", #standard
               "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider", #standard
               "fs.azure.account.oauth2.client.id": vApplicationId,
               "fs.azure.account.oauth2.client.secret": vAuthenticationKey,
               "fs.azure.account.oauth2.client.endpoint": vEndpoint}

    # Mount Data Lake Storage to Databricks File System only if the container is not already mounted
    # First generate a list of all mount points available already via dbutils.fs.mounts()
    # Then it checks the list for the new mount point we are trying to generate.
    if not any(mount.mountPoint == vMountPoint for mount in dbutils.fs.mounts()): 
      dbutils.fs.mount(
        source = vSource,
        mount_point = vMountPoint,
        extra_configs = vConfigs)

    # print the mount point used for troubleshooting in the consuming notebook
    print("Mount Point: " + vMountPoint)

# COMMAND ----------

mount_lake_container('json-files', 'json-normalisation-secret-scope', 'json-normalisation-storage-account-name', 'json-normalisation-application-id', 'json-normalisation-service-principle-password', 'json-normalisation-tenant-id')

# COMMAND ----------

# Read json file
df = spark.read.json('/mnt/datalake_json-files/json-file.json', multiLine=True)

# COMMAND ----------

# Display DataFrame
display(df)

# COMMAND ----------


