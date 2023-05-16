cdc_data_spec = (dg.DataGenerator(spark, rows=1000000, partitions = 10)
    .withColumn('RECID', 'int' , uniqueValues=1000000)
    .withColumn('COMPANYNAME', 'string' , values=['Company1','Company2','Company3'])
    .withColumn('QUANTITY', 'int' , minValue=1, maxValue=5, random=True)
    .withColumn("UPDATE_TIME", "timestamp", expr="current_timestamp()"))

cdc_data_df = cdc_data_spec.build()

cdc_data_df.write.mode("overwrite").saveAsTable("erictome_cdf_delta_sharing.share_data")