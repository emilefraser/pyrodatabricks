# Databricks notebook source
# MAGIC %md
# MAGIC # JSON Normalisation for One Column
# MAGIC 
# MAGIC This notebook outlines a method to flatten a file that has JSON in just one column. A CSV was used in this case but a similar approach can be used for other formats.

# COMMAND ----------

# Imports
from pyspark.sql.functions import concat, lit, from_json, col, explode_outer
from pyspark.sql.types import ArrayType, StructType

# COMMAND ----------

# MAGIC %md
# MAGIC The `mount_lake_container`, `get_json_df_tangent` and `execute_autoflatten` functions can be found in ReferenceArchtectures/Databricks/HelperFunctions/DataLakeHelperFunctions.ipynb in the code-library repo on GopherSquad's Azure DevOps.

# COMMAND ----------

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

def get_json_df_tangent(inputDF, json_column_name, spark_session):
    '''
    Description:
    This function provides the schema of json records and the dataframe to be used for flattening. If this doesnt happen, the source JSON String remains a string and cant be queries like JSON
        :param inputDF: [type: pyspark.sql.dataframe.DataFrame] input dataframe
        :param json_column_name: [type: string] name of the column with json string
        :param spark_session: SparkSession object
        :return df: dataframe to be used for flattening
    '''
    # creating a column transformedJSON to create an outer struct
    df1 = inputDF.withColumn('transformed_json', concat(lit("""{"transformed_json" :"""), inputDF[json_column_name], lit("""}""")))
    json_df = spark_session.read.json(df1.rdd.map(lambda row: row.transformed_json))
    # get schema
    json_schema = json_df.schema
    
    #Return a dataframe with the orignal column name but with proper JSON typed data
    df = df1.drop(json_column_name)\
        .withColumn(json_column_name, from_json(col('transformed_json'), json_schema))\
        .drop('transformed_json')\
        .select(f'{json_column_name}.*', '*')\
        .drop(json_column_name)\
        .withColumnRenamed("transformed_json", json_column_name)
    return df

# COMMAND ----------

def execute_autoflatten(df, json_column_name):
    '''
    Description:
    This function executes the core autoflattening operation

    :param df: [type: pyspark.sql.dataframe.DataFrame] dataframe to be used for flattening
    :param json_column_name: [type: string] name of the column with json string

    :return df: DataFrame containing flattened records
    '''
    # gets all fields of StructType or ArrayType in the nested_fields dictionary
    nested_fields = dict([
        (field.name, field.dataType)
        for field in df.schema.fields
        if isinstance(field.dataType, ArrayType) or isinstance(field.dataType, StructType)
    ])

    # repeat until all nested_fields i.e. belonging to StructType or ArrayType are covered
    while nested_fields:
        # if there are any elements in the nested_fields dictionary
        if nested_fields:
            # get a column
            column_name = list(nested_fields.keys())[0]
            # if field belongs to a StructType, all child fields inside it are accessed
            # and are aliased with complete path to every child field
            if isinstance(nested_fields[column_name], StructType):
                unnested = [col(column_name + '.' + child).alias(column_name + '>' + child) for child in [ n.name for n in  nested_fields[column_name]]]
                df = df.select("*", *unnested).drop(column_name)
            # else, if the field belongs to an ArrayType, an explode_outer is done
            elif isinstance(nested_fields[column_name], ArrayType):
                df = df.withColumn(column_name, explode_outer(column_name))

        # Now that df is updated, gets all fields of StructType and ArrayType in a fresh nested_fields dictionary
        nested_fields = dict([
            (field.name, field.dataType)
            for field in df.schema.fields
            if isinstance(field.dataType, ArrayType) or isinstance(field.dataType, StructType)
        ])

    # renaming all fields extracted with json> to retain complete path to the field
    for df_col_name in df.columns:
        df = df.withColumnRenamed(df_col_name, df_col_name.replace("transformedJSON", json_column_name))
    return df

# COMMAND ----------

# MAGIC %md
# MAGIC Read the CSV file

# COMMAND ----------

mount_lake_container('json-files', 'json-normalisation-secret-scope', 'json-normalisation-storage-account-name', 'json-normalisation-application-id', 'json-normalisation-service-principle-password', 'json-normalisation-tenant-id')

df = spark.read.options(delimiter='|', header=True, multiLine=True, escape='"', quote='"').csv('/mnt/datalake_json-files/json-in-column-hardcore.csv')

# COMMAND ----------

# MAGIC %md
# MAGIC Apply to DataFrame

# COMMAND ----------

df_json = get_json_df_tangent(df, 'info', spark)
df_flat = execute_autoflatten(df_json, 'info')
display(df_flat)
