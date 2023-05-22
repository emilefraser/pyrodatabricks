# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Gets Lotto Draws Info
# MAGIC
# MAGIC The purpose of this layer is to determine which draws there are and retrieve this info

# COMMAND ----------

from datetime import datetime
from pyspark.sql.functions import col, lit, explode, regexp_extract, when
import re

# COMMAND ----------

# Notebook variables
layer_source = "replica"
layer_target = "bronze"

# COMMAND ----------

# temp vars
country="south_africa"
lottery_name="ALL"
provider="ithuba"

# COMMAND ----------

# Gets the current date and reads from replica layer
now = datetime.now()
replica_path = f"/mnt/{layer_source}/object=draw/country={country}/provider={provider}/lottery_name={lottery_name}/year={now.strftime('%Y')}/month={now.strftime('%m')}/day={now.strftime('%d')}"
jsondata = spark.read.format("json").option("inferSchema", True).load(f"{replica_path}/")
display(jsondata)

# COMMAND ----------

df = jsondata.select(col("code"), col("message"), explode(jsondata.videoData))
df=df.select(col("code"), col("message"), col("col.*"))

# check if the format of the alias is either
# powerball-and-powerball-plus-draw-1401
# "692-powerball-and-powerball-plus-draw-08-july-2016")
# rdf=df.withColumn('draw_id', regexp_extract(col('alias'), '(?<=-draw-)([0-9]*)', 1))
# ndf=rdf.withColumn('starts_with_number', regexp_extract(col('alias'), '^([0-9]*)-', 1))
excludes = [130,207,487,503]
excludes2 = [483,487,496,497,491]
df=df.withColumn('draw_id', when(df.id.isin(excludes), lit(-1))
.when(df.id.isin(excludes2), lit(-2))
.when(col('alias').rlike('^[0-9]*-'), regexp_extract(col('alias'), '^([0-9]*)-', 1))
.when(col('alias').rlike('draw-[0-9]*'), regexp_extract(col('alias'), '(?<=-draw-)([0-9]*)', 1))
.otherwise(lit(-9)))

#df.sort_values(by=['Brand'], inplace=True)
#when(df.email.rlike('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'),True).otherwise(False)
display(df.orderBy(col('draw_id')))
# df = result_df.select(explode(col("result.Results")).alias("results"))
# df.select(collapse_columns(df.schema)).show()

# COMMAND ----------

#
#


regexp_extract(lit("powerball-and-powerball-plus-draw-08-july-2016"), '^([0-9]*)$', 1)

# COMMAND ----------



#jsondata.printSchema()
#display(jsondata)



#display(df2)
draw = re.split("draw", str(df2.select(col("alias"))))[1]
display(draw)
#draw=re.split("draw", df2.select(col("alias")))
#df2.withColumn("draw_id", draw)
#display(df2)listFiles = dbutils.fs.ls(bronze_path)
display(listFiles)

# copies data file over to correct path
dbfs cp source_file_path destination_path 

bronze_path}/partition

dbutils.fs.rm(bronze_path, recurse = True)
#listFiles = dbutils.fs.ls(bronze_path)
#display(listFiles)

# COMMAND ----------

listFiles = dbutils.fs.ls(bronze_path)
display(listFiles)

# copies data file over to correct path
dbfs cp source_file_path destination_path 

bronze_path}/partition

dbutils.fs.rm(bronze_path, recurse = True)
#listFiles = dbutils.fs.ls(bronze_path)
#display(listFiles)

# COMMAND ----------



# COMMAND ----------

