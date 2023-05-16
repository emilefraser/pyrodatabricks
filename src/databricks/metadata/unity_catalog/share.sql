CREATE CATALOG IF NOT EXISTS erictome;
USE CATALOG erictome;

CREATE SHARE IF NOT EXISTS ds_cdf_table_share

DESCRIBE SHARE ds_cdf_table_share;

ALTER SHARE ds_cdf_table_share 
ADD TABLE erictome_cdf_delta_sharing.cdf_ds_external
PARTITION (`COMPANYNAME` = "Company2") as cdf_ds_external.Company2;

SHOW ALL IN SHARE ds_cdf_table_share;

CREATE RECIPIENT IF NOT EXISTS erictome;

DESC RECIPIENT erictome;

GRANT SELECT ON SHARE ds_cdf_table_share TO RECIPIENT erictome;