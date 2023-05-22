# Databricks notebook source
# MAGIC %sh
# MAGIC ls /databricks/spark/dbconf/log4j/master-worker
# MAGIC ls /databricks/spark/dbconf/log4j/driver
# MAGIC ls /databricks/spark/dbconf/log4j/executor
# MAGIC ls /databricks/spark/dbconf/log4j/chauffeur
# MAGIC
# MAGIC cat /databricks/spark/dbconf/log4j/driver/log4j2.xml > /dbfs/logs-config/log4j2.xml

# COMMAND ----------

# MAGIC %sh
# MAGIC echo $LOG4J_PATH

# COMMAND ----------

# MAGIC %scala
# MAGIC import com.microsoft.pnp.logging.Log4jConfiguration
# MAGIC
# MAGIC Log4jConfiguration.configure("/dbfs/logs-config/log4j.properties")

# COMMAND ----------

# MAGIC %sh
# MAGIC ls /databricks/spark/dbconf/log4j/driver
# MAGIC cat /databricks/spark/dbconf/log4j/driver/log4j2.xml
# MAGIC
# MAGIC #! /bin/bash
# MAGIC
# MAGIC set -euxo pipefail
# MAGIC
# MAGIC echo "Running on the driver? ${DB_IS_DRIVER}"
# MAGIC echo "Driver ip: ${DB_DRIVER_IP}"
# MAGIC
# MAGIC cat >>/databricks/spark/dbconf/log4j/driver/log4j2.properties <<EOL
# MAGIC
# MAGIC appender.customFile.type = RollingFile
# MAGIC appender.customFile.name = customFile
# MAGIC appender.customFile.layout.type = PatternLayout
# MAGIC appender.customFile.layout.pattern = [spark] %d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n%ex
# MAGIC appender.customFile.filePattern = logs/log4j.custom.%d{yyyy-MM-dd-HH}.log.gz
# MAGIC appender.customFile.policies.type = Policies
# MAGIC appender.customFile.policies.time.type = TimeBasedTriggeringPolicy
# MAGIC appender.customFile.policies.time.interval = 1
# MAGIC appender.customFile.fileName = logs/stdout.custom-active.log
# MAGIC
# MAGIC logger.custom=DEBUG, customFile
# MAGIC logger.custom.name = com.custom
# MAGIC logger.custom.additivity = true

# COMMAND ----------

# Databricks notebook source
from pyspark.sql import SparkSession
from typing import Optional

NOTEBOOK_PATH = (
    dbutils.notebook.entry_point.getDbutils()
    .notebook()
    .getContext()
    .notebookPath()
    .get()
)
FORMATTED_NOTEBOOK_PATH = (
    NOTEBOOK_PATH.lower().replace("/", ".") + "."
)  # add trailing dot


class LoggerProvider:
    def get_logger(self, spark: SparkSession, custom_prefix: Optional[str] = ""):
        log4j_logger = spark._jvm.org.apache.log4j  # noqa
        return log4j_logger.LogManager.getLogger(custom_prefix + self.__full_name__())

    def __full_name__(self):
        klass = self.__class__
        module = klass.__module__
        if module == "__builtin__":
            return klass.__name__  # avoid outputs like '__builtin__.str'
        return module + "." + klass.__name__


# COMMAND ----------

logger = LoggerProvider().get_logger(spark, custom_prefix="notebooks" + FORMATTED_NOTEBOOK_PATH)

# COMMAND ----------


# COMMAND ----------

# COMMAND ----------

logger = LoggerProvider().get_logger(spark, custom_prefix="notebooks" + FORMATTED_NOTEBOOK_PATH)
logger.info("some info message")
logger.warn("some warning message")
logger.fatal("some fatal message")


# COMMAND ----------

print(logger.getLevel())
print(logger)

# COMMAND ----------

# MAGIC %scala
# MAGIC println(System.getenv.get("MASTER"))        // 10.139.64.5
# MAGIC println(System.getenv.get("SPARK_LOCAL_IP")) // 10.139.64.5
# MAGIC println(System.getenv.get("SPARK_PUBLIC_DNS"))
# MAGIC println(System.getenv.get("DB_DRIVER_IP"))
# MAGIC println(System.getenv.get("SPARK_PUBLIC_DNS"))

# COMMAND ----------

# MAGIC %sh 
# MAGIC
# MAGIC printenv

# COMMAND ----------

from requests import get
 
ip = get('https://api.ipify.org').text
print('My public IP address is:', ip)   # 4.221.8.7   
4.211.8.7

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC ifconfig

# COMMAND ----------

# MAGIC %sh
# MAGIC echo $DB_IS_DRIVER