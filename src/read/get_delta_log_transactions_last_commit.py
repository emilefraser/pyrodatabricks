def display_delta_log(table, version=None):
    if not version:
        version = spark.conf.get("spark.databricks.delta.lastCommitVersionInSession")
    version_str = str(int(version)).zfill(20)
    file = f"{DA.paths.user_db}/{table}/_delta_log/{version_str}.json"
    print("Showing: "+file)
    display(spark.read.json(file))

# used with
display_delta_log("bronze")