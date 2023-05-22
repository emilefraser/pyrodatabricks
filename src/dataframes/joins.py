# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC # Joins
# MAGIC 
# MAGIC - trigger a large amount of data movement
# MAGIC - At the heart of these transformations is how Spark computes what data to produce, what keys and associated data to write to the disk, and how to transfer those keys and data to nodes as part of operations like groupBy(), join(), agg(), sortBy(), and reduceByKey(). This movement is commonly referred to as the shuffle.
# MAGIC 
# MAGIC Spark has 5 ways of joining:
# MAGIC 1. Broadcast Hash Join (BHJ or map side only join)
# MAGIC 2. Shuffle Hash Join (SHJ)
# MAGIC 3. Broadcast Nested Loop Join (BNLJ)
# MAGIC 4. Shuffle-&-Replicated Nested Loop Join (Cartesian Product Join)

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC # Broadcast Join
# MAGIC 
# MAGIC NOTE
# MAGIC In this code we are forcing Spark to do a broadcast join, but it will resort to this type of join by default if the size of the smaller data set is below the 
# MAGIC `spark.sql.autoBroadcastJoinThreshold = 10MB`

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC // BHJ
# MAGIC import org.apache.spark.sql.functions.broadcast
# MAGIC 
# MAGIC val joinedDF = playersDF.join(broadcast(clubsDF), "key1 === key2")

# COMMAND ----------

from pyspark.sql.functions import broadcast

joinedDF = playersDF.join(broadcast(clubsDF), "key1 = key2")
# Databricks notebook source
from pyspark.sql import Row
from datetime import datetime
from pyspark.sql.types import StructField, StructType, StringType, DateType, IntegerType

peopleSchema = StructType([
  StructField("Name",   StringType(),  True),
  StructField("Family", IntegerType(), True),
  StructField("dob",    DateType(),    False)
])
dateformat = "%d-%m-%Y"

rows = [
  Row("Shaun",  1, datetime.strptime('25-01-1977', dateformat)),
  Row("Sarah",  1, datetime.strptime('10-01-1981', dateformat)),
  Row("Finley", 1, datetime.strptime('30-10-2017', dateformat)),
  
  Row("Paul",   2, datetime.strptime('12-04-1976', dateformat)),
  Row("Simon",  2, datetime.strptime('24-05-1978', dateformat))
]

dfp = spark.createDataFrame(rows, peopleSchema)
display(dfp)

# COMMAND ----------

familySchema = StructType([
  StructField("Name",     StringType(),  True),
  StructField("Family",   IntegerType(), True),
  StructField("PostCode", StringType(),  False)
])
dateformat = "%d-%m-%Y"

rows = [
  Row("Ryan",      1, "BS15 9RH"),
  Row("Pieman",    1, "YO16 6RE")
]

dff = spark.createDataFrame(rows, familySchema)
display(dff)

# COMMAND ----------

# the join column problem
from pyspark.sql.functions import expr, col, column

join = "Family = Family"

dfj = dfp.join(dff, join, "inner").drop(dff.Family)
display(dfj.select("Family"))

# COMMAND ----------

# DBTITLE 1,Implied Join - not this automatically reduces join columns to a single column
from pyspark.sql.functions import expr, col, column

dfj = dfp.join(dff, "Family", "inner")
display(dfj)


# COMMAND ----------

# DBTITLE 1,Explicit Join
from pyspark.sql.functions import expr, col, column

join = dfp["Family"] == dff["Family"]

dfj = dfp.join(dff, join, "inner")
display(dfj)

# COMMAND ----------

# DBTITLE 1,Explicit Join with String - will fail because of column abiguity
# the join column problem
from pyspark.sql.functions import expr, col, column

join = "Family = Family"

dfj = dfp.join(dff, join, "inner")
display(dfj)

# COMMAND ----------

# DBTITLE 1,Explicit Join with Expression - will fail because of column abiguity
# the join column problem
from pyspark.sql.functions import expr, col, column

join = dfp["Family"] == dff["Family"]

dfj = dfp.join(dff, join, "inner")
display(dfj.select("Family"))

# COMMAND ----------

# DBTITLE 1,Explicit Join with Expression - have to drop the column manually
# the join column problem
from pyspark.sql.functions import expr, col, column

join = dfp.Family == dff.Family

dfj = dfp.join(dff, join, "inner").drop(dff.Family)
display(dfj.select("Family"))
# -*- coding: utf-8 -*-
"""
author SparkByExamples.com
"""

from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder \
          .appName('SparkByExamples.com') \
          .getOrCreate()
#EMP DataFrame
empData = [(1,"Smith",10), (2,"Rose",20),
    (3,"Williams",10), (4,"Jones",30)
  ]
empColumns = ["emp_id","name","emp_dept_id"]
empDF = spark.createDataFrame(empData,empColumns)
empDF.show()

#DEPT DataFrame
deptData = [("Finance",10), ("Marketing",20),
    ("Sales",30),("IT",40)
  ]
deptColumns = ["dept_name","dept_id"]
deptDF=spark.createDataFrame(deptData,deptColumns)  
deptDF.show()

#Address DataFrame
addData=[(1,"1523 Main St","SFO","CA"),
    (2,"3453 Orange St","SFO","NY"),
    (3,"34 Warner St","Jersey","NJ"),
    (4,"221 Cavalier St","Newark","DE"),
    (5,"789 Walnut St","Sandiago","CA")
  ]
addColumns = ["emp_id","addline1","city","state"]
addDF = spark.createDataFrame(addData,addColumns)
addDF.show()

#Join two DataFrames
empDF.join(addDF,empDF["emp_id"] == addDF["emp_id"]).show()

#Drop duplicate column
empDF.join(addDF,["emp_id"]).show()

#Join Multiple DataFrames
empDF.join(addDF,["emp_id"]) \
     .join(deptDF,empDF["emp_dept_id"] == deptDF["dept_id"]) \
     .show()

#Using Where for Join Condition
empDF.join(deptDF).where(empDF["emp_dept_id"] == deptDF["dept_id"]) \
    .join(addDF).where(empDF["emp_id"] == addDF["emp_id"]) \
    .show()
    
#SQL
empDF.createOrReplaceTempView("EMP")
deptDF.createOrReplaceTempView("DEPT")
addDF.createOrReplaceTempView("ADD")

spark.sql("select * from EMP e, DEPT d, ADD a " + \
    "where e.emp_dept_id == d.dept_id and e.emp_id == a.emp_id") \
    .show()
    
#
df1 = spark.createDataFrame(
    [(1, "A"), (2, "B"), (3, "C")],
    ["A1", "A2"])

df2 = spark.createDataFrame(
    [(1, "F"), (2, "B")], 
    ["B1", "B2"])

df = df1.join(df2, (df1.A1 == df2.B1) & (df1.A2 == df2.B2))
df.show()