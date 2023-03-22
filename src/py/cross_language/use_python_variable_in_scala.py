# Python part
srcRecCount = batdf.count()
spark.conf.set("mydata.srcRecCount", str(srcRecCount))

# Scala part
val srcRecCount = spark.conf.get("mydata.srcRecCount")
dbutils.notebook.exit(
  s"""{'date':'$endPartDelta', 'srcRecCount':'$srcRecCount'}""")