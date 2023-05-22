create table erictome_cdf_delta_sharing.cdf_ds_external
partitioned by (COMPANYNAME)
   as
   select 
    RECID,
    COMPANYNAME,
    QUANTITY,
    UPDATE_TIME,
    _change_type change_type,
    _commit_version commit_version,
    _commit_timestamp commit_timestamp
   from table_changes('erictome_cdf_delta_sharing.share_data', 0);