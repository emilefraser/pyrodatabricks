df = spark.read.format('csv').load(
  '/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv',
  header=True,
  inferSchema=True
)
dbutils.data.summarize(df)