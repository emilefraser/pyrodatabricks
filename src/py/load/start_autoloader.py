def load_gym_logs():
    query = (spark.readStream
                  .format("cloudFiles")
                  .option("cloudFiles.format", "json")
                  .option("cloudFiles.schemaLocation", f"{DA.paths.checkpoints}/gym_mac_logs_schema")
                  # .option("cloudFiles.useNotifications","true") # Set this option for file notification mode
                  .load(DA.paths.gym_mac_logs_json)
                  .writeStream
                  .format("delta")
                  .option("checkpointLocation", f"{DA.paths.checkpoints}/gym_mac_logs")
                  .trigger(availableNow=True)
                  .table("gym_mac_logs"))
    
    query.awaitTermination()