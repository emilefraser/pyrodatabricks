# Databricks notebook source
#  Replace with your container and storage account:  "wasbs://<container>@<storage account>.blob.core.windows.net/"
pathPrefix = "wasbs://ted@vpldb.blob.core.windows.net/"
path = pathPrefix + "ted_main.csv"

# COMMAND ----------

# MAGIC %md
# MAGIC # Ted Talks Data set
# MAGIC
# MAGIC Taken from https://www.kaggle.com/rounakbanik/ted-talks/data

# COMMAND ----------

import csv
import StringIO

# Load the data as one big string
# We do this because Spark is unable to parse the CSV correctly due to some escaping
text = sc.wholeTextFiles(path).take(1)[0][1]
# Use Python's csv module to parse the content
lines = [v for v in csv.reader(StringIO.StringIO(text.encode('utf8', 'ignore')))]
# Take the first row as column names
columnNames = lines[0]
# Take the rest of the rows as content
content = sc.parallelize(lines[1:])
# Filter out rows that wouldn't have the right number of columns
compliant = content.filter(lambda v: len(v)==len(columnNames))
# Map list-rows to dictionaries using the column names
talkDict = compliant.map(lambda r: dict(zip(columnNames, r)))

# COMMAND ----------

def parse(singleQuotedJson):
  import ast
  
  return ast.literal_eval(singleQuotedJson)
  
def reworkFields(d):
  # Parse integers since Python's CSV parser only parse strings
  d['comments'] = int(d['comments'])
  d['duration'] = int(d['duration'])
  d['film_date'] = int(d['film_date'])
  d['num_speaker'] = int(d['num_speaker'])
  d['published_date'] = int(d['published_date'])
  d['views'] = int(d['views'])
  
  # Parse json columns (into dictionaries)
  d['ratings'] = parse(d['ratings'])
  d['related_talks'] = parse(d['related_talks'])
  d['tags'] = parse(d['tags'])

  return d

def cleanDenormalizedAttributes(dict):
  # Remove denormalized properties
  del(dict['ratings'])
  del(dict['related_talks'])
  del(dict['tags'])
  
  return dict

# COMMAND ----------

# Rework some fields
cleanFields = talkDict.map(lambda r: reworkFields(r))
# Extract ratings as a separate RDD linked to the talks one with the talk name
ratings = cleanFields.flatMap(lambda d: [{'talkName':d['name'], 'id':r['id'], 'name':r['name'], 'count':r['count']} for r in d['ratings']])
# Extract related talks, similarly linked to talk name
relatedTalks = cleanFields.flatMap(lambda d: [{'talkName':d['name'], 'relatedTalkName':r['title']} for r in d['related_talks']])
# Extract tags, similarly linked to talk name
tags = cleanFields.flatMap(lambda d: [{'talkName':d['name'], 'tag':t} for t in d['tags']])
# Normalize the talkDict by removing denormalized attributes
normalizedTalks = cleanFields.map(lambda d:  cleanDenormalizedAttributes(d))

# COMMAND ----------

from pyspark.sql import Row

# Create data frames, cache them and register them as temp views
normalizedTalksDf = spark.createDataFrame(normalizedTalks.map(lambda d: Row(**d)))
normalizedTalksDf.cache()
normalizedTalksDf.createOrReplaceTempView("talks")

ratingsDf = spark.createDataFrame(ratings.map(lambda d: Row(**d)))
ratingsDf.cache()
ratingsDf.createOrReplaceTempView("ratings")

relatedTalksDf = spark.createDataFrame(relatedTalks.map(lambda d: Row(**d)))
relatedTalksDf.cache()
relatedTalksDf.createOrReplaceTempView("relatedTalks")

tagsDf = spark.createDataFrame(tags.map(lambda d: Row(**d)))
tagsDf.cache()
tagsDf.createOrReplaceTempView("tags")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC (
# MAGIC   SELECT COUNT(*)
# MAGIC   FROM talks
# MAGIC ) AS talkCount,
# MAGIC (
# MAGIC   SELECT COUNT(*)
# MAGIC   FROM ratings
# MAGIC ) AS ratingTalkCount,
# MAGIC (
# MAGIC   SELECT COUNT(*)
# MAGIC   FROM relatedTalks
# MAGIC ) AS relatedTalkCount,
# MAGIC (
# MAGIC   SELECT COUNT(*)
# MAGIC   FROM tags
# MAGIC ) AS tagCount

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT title, main_speaker, views, ROUND(1000000*comments/views, 1) AS commentsPerMillionViews
# MAGIC FROM talks
# MAGIC ORDER BY views DESC
# MAGIC LIMIT 10

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT ROUND(AVG(t.views)) as avgViews, tg.tag
# MAGIC FROM talks AS t
# MAGIC INNER JOIN tags tg ON tg.talkName=t.name
# MAGIC GROUP BY tg.tag
# MAGIC ORDER BY avgViews DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT name, SUM(count) AS ratingCount
# MAGIC FROM ratings
# MAGIC GROUP BY name
# MAGIC ORDER BY ratingCount DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT t.title, t.main_speaker, t.views, r.count
# MAGIC FROM talks AS t
# MAGIC INNER JOIN ratings AS r ON r.talkName = t.name AND r.name="Inspiring"
# MAGIC ORDER BY r.count DESC

# COMMAND ----------

