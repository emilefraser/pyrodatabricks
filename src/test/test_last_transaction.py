last_version = spark.sql("DESCRIBE HISTORY beans").orderBy(F.col("version").desc()).first()

assert last_version["operation"] == "MERGE", "Transaction should be completed as a merge"