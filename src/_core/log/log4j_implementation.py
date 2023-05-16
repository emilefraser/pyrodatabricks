# Databricks notebook source
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from typing import Optional
import logging
import yaml
import pathlib
import os

class LoggerProvider:
    def get_logger(self, spark: SparkSession, custom_prefix: Optional[str] = ""):
        log4j_logger = spark._jvm.org.apache.log4j  # noqa
        LOGGER = log4j_logger.LogManager.getLogger(custom_prefix + self.__full_name__())
        LOGGER.setLevel(log4j_logger.Level.INFO)
        #java -Dlog4j.configuration=file:/path/to/log4j.properties myApp


        return LOGGER

    def __full_name__(self):
        klass = self.__class__
        module = klass.__module__
        if module == "__builtin__":
            return klass.__name__  # avoid outputs like '__builtin__.str'
        return module + "." + klass.__name__

# COMMAND ----------
sc = SparkContext('local')
sc.setLogLevel('INFO')
spark = SparkSession.builder.appName("EMILETEST").getOrCreate()

#export SPARK_CONF_DIR="$(PWD)/src/_core/config/local/log4j.properties"


logger = LoggerProvider().get_logger(
    spark, custom_prefix="notebooks" #+ FORMATTED_NOTEBOOK_PATH
)


# COMMAND ----------
#config = yaml.safe_load(pathlib.Path('/home/pyromaniac/repos/pyrodatabricks/src/_core/config/local/log4j.properties').read_text())
#logger.conf=config
#logger.configuration='/home/pyromaniac/repos/pyrodatabricks/src/_core/config/local/log4j.properties'
#logger.addAppender("[spark][%p][%d{yy/MM/dd HH:mm:ss}][%c][%m]%n")
logger.info("some info message")
logger.warn("some warning message") 
logger.fatal("some fatal message")

# # COMMAND ----------
# import os
# os.environ["DEBUSSY"] = "1"
# to set the variable DEBUSSY to the string 1.

# To access this variable later, simply use

