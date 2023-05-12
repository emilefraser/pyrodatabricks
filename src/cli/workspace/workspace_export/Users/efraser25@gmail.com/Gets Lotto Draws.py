# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Gets Lotto Draws
# MAGIC
# MAGIC The purpose of this layer is to land the json return text of the LotteryInfo and use that to loop through the Draws and Draw Events

# COMMAND ----------

import requests
import json
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode, from_json, schema_of_json
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql import Row

# COMMAND ----------

# MAGIC %run "./Well Known"

# COMMAND ----------

# Notebook variables
layer = "replica"

# COMMAND ----------

# Loop through the Lottery Dictionary
# gets unique active links and determine whether they should be scraped
# need to read from lotterie and providers 
# then get distinct dictionary
lottery_list = list(set(val for dic in lotteries for val in lotteries.values()))
lottery_list_active = [(i.LotteryProvider.provider_code, i.lottery_code, i.lottery_uri, i.LotteryProvider.provider_uri) for i in lottery_list if i.is_active == True]
lottery_list_active = (list(set([(i[1], i[2]) if i[2] != None else (i[0]+"|ALL", i[3])  for i in lottery_list_active])))
#[print(i) for i in lottery_list_active]

# for loop and then rest of code
for lottery in lottery_list_active:
    now = datetime.now()
    country = lottery[0].split("|")[0]
    provider = lottery[0].split("|")[1]
    lottery_name = lottery[0].split("|")[2]

    ## gets path here based on values
    replica_path = f"/mnt/{layer}/object=draw/country={country}/provider={provider}/lottery_name={lottery_name}/year={now.strftime('%Y')}/month={now.strftime('%m')}/day={now.strftime('%d')}"
    replica_file_name = f"draw_{now.strftime('%Y')}{now.strftime('%m')}{now.strftime('%d')}.json"

    # gets the lottery data
    api_response = requests.get(lottery[1])
    df = spark.read.json(sc.parallelize([api_response.text]))

    # writes out to single partition with overwrite
    (
    df.coalesce(1)
        .write
        .mode("overwrite")
        .json(f"{replica_path}/partition")
    )

    # moves actual data file and deletes partitioning files
    files_partition= dbutils.fs.ls(f"{replica_path}/partition")
    replicated_file = [ i for i in files_partition if i.path.endswith(".json") ]
    dbutils.fs.cp(replicated_file[0].path, f"{replica_path}/{replica_file_name}")
    dbutils.fs.rm(f"{replica_path}/partition", recurse=True)


# COMMAND ----------

print("Gets Lotto Draws Completed")