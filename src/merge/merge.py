deltaTable = DeltaTable.forName(spark, 'erictome_cdf_delta_sharing.share_data')

(deltaTable.alias('existing') 
  .merge(
    cdc_inc_data_df.alias('updates'),
    'existing.RECID = updates.RECID'
  ) 
  .whenMatchedUpdate(set =
    {
      "COMPANYNAME": "updates.COMPANYNAME",
      "QUANTITY": "updates.QUANTITY",
      "UPDATE_TIME": "updates.UPDATE_TIME"
    }
  ) 
  .whenNotMatchedInsert(values =
    {
      "COMPANYNAME": "updates.COMPANYNAME",
      "QUANTITY": "updates.QUANTITY",
      "UPDATE_TIME": "updates.UPDATE_TIME"
    }
  ) 
  .execute())