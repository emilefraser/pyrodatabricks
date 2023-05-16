# Databricks notebook source
# MAGIC %md
# MAGIC ## Description 
# MAGIC Trying to run cli code to improt notebooks from the databricks workspace

# COMMAND ----------

dbutils.help()

# COMMAND ----------

# MAGIC %sh
# MAGIC ls

# COMMAND ----------

myfiles = !fs ls
print(myfiles)

# COMMAND ----------

print(myfiles)

# COMMAND ----------

# MAGIC %fs ls

# COMMAND ----------

# MAGIC %%capture abc
# MAGIC %fs ls

# COMMAND ----------

xyz = !fs ls

# COMMAND ----------

type(abc)

# COMMAND ----------

type(xyz)

# COMMAND ----------

# MAGIC %bash 
# MAGIC echo $xyz

# COMMAND ----------

# MAGIC %pip install databricks-cli

# COMMAND ----------

# MAGIC %sh databricks workspace list

# COMMAND ----------

# MAGIC %history

# COMMAND ----------

# MAGIC %fs

# COMMAND ----------

# MAGIC %ls

# COMMAND ----------

# MAGIC %notebook ....

# COMMAND ----------

# MAGIC %%sh¶
# MAGIC %%sh script magic
# MAGIC
# MAGIC Run cells with sh in a subprocess.
# MAGIC
# MAGIC This is a shortcut for %%script sh

# COMMAND ----------

# MAGIC %xmode¶
# MAGIC Switch modes for the exception handlers.

# COMMAND ----------

# MAGIC %%script¶

# COMMAND ----------

# MAGIC %script bash
# MAGIC for i in 1 2 3; do
# MAGIC echo $i
# MAGIC done

# COMMAND ----------

# MAGIC %%html¶
# MAGIC %html [--isolated]

# COMMAND ----------

# MAGIC %%capture¶
# MAGIC %capture [--no-stderr] [--no-stdout] [--no-display] [output]
# MAGIC run the cell, capturing stdout, stderr, and IPython’s rich display() calls.

# COMMAND ----------

# MAGIC %whos

# COMMAND ----------

# MAGIC %who_ls

# COMMAND ----------



# COMMAND ----------

# MAGIC %unalias

# COMMAND ----------

# MAGIC %timeit¶

# COMMAND ----------

# MAGIC %time¶

# COMMAND ----------

# MAGIC %tb

# COMMAND ----------

# MAGIC %system¶

# COMMAND ----------

# MAGIC %rerun

# COMMAND ----------

# MAGIC %pwd

# COMMAND ----------

# MAGIC %pycat

# COMMAND ----------

# MAGIC %pinfo %pfile

# COMMAND ----------

# MAGIC %magic

# COMMAND ----------

# MAGIC %lsmagic