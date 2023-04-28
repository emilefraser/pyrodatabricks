
def process_bronze():
    query = (spark.readStream
                  .format("cloudFiles")
                  .option("cloudFiles.format", "json")
                  .option("cloudFiles.schemaLocation", f"{DA.paths.checkpoints}/bronze_schema")
                  .load(DA.paths.source_daily)
                  .join(F.broadcast(date_lookup_df), F.to_date((F.col("timestamp")/1000).cast("timestamp")) == F.col("date"), "left")
                  .writeStream
                  .option("checkpointLocation", f"{DA.paths.checkpoints}/bronze")
                  .partitionBy("topic", "week_part")
                  .trigger(availableNow=True)
                  .table("bronze"))
    
    query.awaitTermination()


process_bronze()