# Databricks notebook source
import requests 
import json 
import pandas as pd 

# COMMAND ----------

city = "Toronto"
apiKey = "xxx" # replace with your own API key# 
apiURL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric"

r = requests.get(apiURL)
r_json = r.json() 

pandas_df = pd.json_normalize(r_json)
spark_df = spark.createDataFrame(pandas_df)
display(spark_df)

# COMMAND ----------

spark_df.printSchema()

# COMMAND ----------

(
spark_df.write
        .format("delta")
        .mode("overwrite")
        .saveAsTable("default.t1_bronze_weather_reading")
)
