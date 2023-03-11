// Databricks notebook source exported at Sun, 19 Jun 2016 11:03:13 UTC
// MAGIC %md
// MAGIC 
// MAGIC # [Scalable Data Science](http://www.math.canterbury.ac.nz/~r.sainudiin/courses/ScalableDataScience/)
// MAGIC 
// MAGIC 
// MAGIC ### prepared by [Raazesh Sainudiin](https://nz.linkedin.com/in/raazesh-sainudiin-45955845) and [Sivanand Sivaram](https://www.linkedin.com/in/sivanand)
// MAGIC 
// MAGIC *supported by* [![](https://raw.githubusercontent.com/raazesh-sainudiin/scalable-data-science/master/images/databricks_logoTM_200px.png)](https://databricks.com/)
// MAGIC and 
// MAGIC [![](https://raw.githubusercontent.com/raazesh-sainudiin/scalable-data-science/master/images/AWS_logoTM_200px.png)](https://www.awseducate.com/microsite/CommunitiesEngageHome)

// COMMAND ----------

// MAGIC %md
// MAGIC The [html source url](https://raw.githubusercontent.com/raazesh-sainudiin/scalable-data-science/master/db/week4/07_UnsupervisedClusteringKMeans_1MSongs/012_1MSongsKMeans_Intro.html) of this databricks notebook and its recorded Uji ![Image of Uji, Dogen's Time-Being](https://raw.githubusercontent.com/raazesh-sainudiin/scalable-data-science/master/images/UjiTimeBeingDogen.png "uji"):
// MAGIC 
// MAGIC [![sds/uji/week4/08_MLIntro/016_DecisionTrees_HandWrittenDigitRecognition](http://img.youtube.com/vi/_Lxtxmn0L-w/0.jpg)](https://www.youtube.com/v/_Lxtxmn0L-w?rel=0&autoplay=1&modestbranding=1&start=4697&end=4823)

// COMMAND ----------

// MAGIC %md
// MAGIC **SOURCE:** This is the scala version of the python notebook from the databricks Community Edition that has been added to this databricks shard at [Workspace -> scalable-data-science -> xtraResources -> dbCE -> MLlib -> unsupervised -> clustering -> k-means -> 1MSongsPy_ETLExploreModel](/#workspace/scalable-data-science/xtraResources/dbCE/MLlib/unsupervised/clustering/k-means/1MSongsPy_ETLExploreModel) as extra resources for this project-focussed course [Scalable Data Science](http://www.math.canterbury.ac.nz/~r.sainudiin/courses/ScalableDataScience/).

// COMMAND ----------

// MAGIC %md
// MAGIC #Data Science with Apache Spark and Scala in Databricks

// COMMAND ----------

// MAGIC %md 
// MAGIC When you first hear a song, do you ever categorize it as slow or fast in your head? Is it even a valid categorization? If so, can one do it automatically? I have always wondered about that. That is why I got excited when I learned about the [Million Songs Dataset](million song dataset challenge). 
// MAGIC 
// MAGIC In this tutorial we will walk through a practical example of a data science project with Apache Spark in Python. We are going to parse, explore and model a sample from the million songs dataset stored on distributed storage. This tutorial is organized into three sections:
// MAGIC 
// MAGIC 1. ETL: Parses raw texts and creates a cached table
// MAGIC 2. Explore: Explores different aspects of the songs table using graphs
// MAGIC 3. Model: Uses SparkML to cluster songs based on some of their attributes
// MAGIC 
// MAGIC ![End to End Data Science](http://training.databricks.com/databricks_guide/end-to-end.png)
// MAGIC 
// MAGIC 
// MAGIC The goal of this tutorial is to prepare you for real world data science projects. Make sure you go through the tutorial in the above order and use the exercises to make yourself familiar further with the API. Also make sure you run these notebooks on a **1.6.x** cluster.

// COMMAND ----------

// MAGIC %md
// MAGIC ### 1. ETL
// MAGIC 
// MAGIC The first step of most data science projects is extracting, transforming and loading data into well formated tables. Our example starts with ETL as well. By following the ETL noteboook you can expect to learn about following Spark concepts:
// MAGIC * RDD: Resilient Distributed Dataset
// MAGIC * Reading and transforming RDDs
// MAGIC * Schema in Spark
// MAGIC * Spark DataFrame
// MAGIC * Temp tables
// MAGIC * Caching tables

// COMMAND ----------

// MAGIC %md
// MAGIC ### 2. Explore
// MAGIC Exploratory analysis is a key step in any real data project. Data scientists use variety of tools to explore and visualize their data. In the second notebook of this tutorial we introduce several tools in Python and Databricks notebooks that can help you visually explore your large data. By reading this notebook and finishing its exercises you will become familiar with:
// MAGIC * How to view the schema of a table
// MAGIC * How to display ggplot and matplotlib figures in Notebooks
// MAGIC * How to summarize and visualize different aspects of large datasets
// MAGIC * How to sample and visualize large data

// COMMAND ----------

// MAGIC %md
// MAGIC ### 3. Model
// MAGIC The end goal of many data scientists is producing useful models. These models are often used for prediction of new and upcoming events in production. In our third notebook we construct a simple K-means clustering model. In this notebook you will learn about:
// MAGIC * Feature transformation
// MAGIC * Fitting a model using SparkML API
// MAGIC * Applying a model to data
// MAGIC * Visualizing model results
// MAGIC * Model tuning

// COMMAND ----------

// MAGIC %md
// MAGIC 
// MAGIC # [Scalable Data Science](http://www.math.canterbury.ac.nz/~r.sainudiin/courses/ScalableDataScience/)
// MAGIC 
// MAGIC 
// MAGIC ### prepared by [Raazesh Sainudiin](https://nz.linkedin.com/in/raazesh-sainudiin-45955845) and [Sivanand Sivaram](https://www.linkedin.com/in/sivanand)
// MAGIC 
// MAGIC *supported by* [![](https://raw.githubusercontent.com/raazesh-sainudiin/scalable-data-science/master/images/databricks_logoTM_200px.png)](https://databricks.com/)
// MAGIC and 
// MAGIC [![](https://raw.githubusercontent.com/raazesh-sainudiin/scalable-data-science/master/images/AWS_logoTM_200px.png)](https://www.awseducate.com/microsite/CommunitiesEngageHome)