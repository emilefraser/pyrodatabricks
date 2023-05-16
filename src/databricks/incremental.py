cdc_inc_data_spec = (dg.DataGenerator(spark, rows=100000, partitions = 1)
    .withColumn('RECID', 'int' , uniqueValues=1000000)
    .withColumn('COMPANYNAME', 'string' , values=['Company1','Company2','Company3'])
    .withColumn('QUANTITY', 'int' , minValue=5, maxValue=10, random=True)
    .withColumn("UPDATE_TIME", "timestamp", expr="current_timestamp()"))

cdc_inc_data_df = cdc_inc_data_spec.build()