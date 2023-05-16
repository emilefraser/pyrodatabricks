// Databricks notebook source
// MAGIC %md
// MAGIC # SparkSession 
// MAGIC
// MAGIC In earlier versions of spark, spark context was entry point for Spark.Essentially, SparkContext allows your application to access the cluster through a resource manager. For every other API,we needed to use different contexts.For streaming, we needed StreamingContext, for SQL sqlContext and for hive HiveContext.HiveContext is a super set of SQLContext that you would need if you want to access Hive tables, or to use richer functionalities such as the window operation, and the trade-off is that HiveContext requires many dependencies to run.
// MAGIC
// MAGIC So in Spark 2.x, we have a new entry point for DataSet and Dataframe API’s called as Spark Session.
// MAGIC
// MAGIC SparkSession is essentially combination of SQLContext, HiveContext and future StreamingContext. All the API’s available on those contexts are available on spark session also. Spark session internally has a spark context for actual computation.

// COMMAND ----------

// MAGIC %md
// MAGIC ### Creating a SparkSession
// MAGIC
// MAGIC A SparkSession can be created using a builder pattern. The builder automatically reuse an existing SparkContext if one exists and creates a SparkContext if it does not exist. Configuration options set in the builder are automatically propagated to Spark and Hadoop during I/O.

// COMMAND ----------

// A SparkSession can be created using a builder pattern
import org.apache.spark.sql.SparkSession
val sparkSession = SparkSession.builder
  .master("local")
  .appName("Jarvis-Application")
  .getOrCreate()

// COMMAND ----------

// MAGIC %md
// MAGIC In Databricks notebooks and Spark REPL, the SparkSession has been created automatically and assigned to variable `spark`. To get the exising session, use getOrCreate method to get the session.

// COMMAND ----------

   var spark=SparkSession.builder().getOrCreate()

// COMMAND ----------

spark

// COMMAND ----------

//Check the version of the Spark
spark.version
//Get a spark context out of SparkSession
var sc=spark.sparkContext
//Get a sql context
var sqlcontext =spark.sqlContext


// COMMAND ----------

// MAGIC %md
// MAGIC To exit the spark session , use close method before exiting from the spark application

// COMMAND ----------

//spark.close()
val tables=spark.catalog.listTables()
display(tables)

// COMMAND ----------

// MAGIC %md
// MAGIC ### Unified entry point for reading data
// MAGIC
// MAGIC SparkSession is the entry point for reading data, similar to the old SQLContext.read.

// COMMAND ----------

val jsonData = spark.read.json("/home/webinar/person.json")

// COMMAND ----------

display(jsonData)

// COMMAND ----------

// MAGIC %md
// MAGIC ### Running SQL queries
// MAGIC
// MAGIC SparkSession can be used to execute SQL queries over data, getting the results back as a DataFrame (i.e. Dataset[Row]).

// COMMAND ----------

display(spark.sql("select * from person"))

// COMMAND ----------

// MAGIC %md
// MAGIC ### Working with config options
// MAGIC
// MAGIC SparkSession can also be used to set runtime configuration options, which can toggle optimizer behavior or I/O (i.e. Hadoop) behavior.

// COMMAND ----------

spark.conf.set("spark.some.config", "abcd")

// COMMAND ----------

spark.conf.get("spark.some.config")

// COMMAND ----------

// MAGIC %md
// MAGIC And config options set can also be used in SQL using variable substitution.

// COMMAND ----------

// MAGIC %sql select "${spark.some.config}"

// COMMAND ----------

// MAGIC %md
// MAGIC ### Working with metadata directly
// MAGIC
// MAGIC SparkSession also includes a `catalog` method that contains methods to work with the metastore (i.e. data catalog). Methods there return Datasets so you can use the same Dataset API to play with them.

// COMMAND ----------

// To get a list of tables in the current database
val tables = spark.catalog.listTables()