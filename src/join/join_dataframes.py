# TODO
from pyspark.sql import functions as F
json_df = spark.read.json(DA.paths.source_daily)
 
joined_df = (json_df.join(F.broadcast(date_lookup_df),
                            F.to_date((F.col("timestamp")/1000).cast("timestamp")) == F.col("date"),
                          "left"))
 
display(joined_df)