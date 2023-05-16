CREATE OR REFRESH STREAMING LIVE TABLE customers
COMMENT "The customers buying finished products, ingested from retail-org/customers."
AS SELECT * FROM cloud_files("${datasets_path}/retail-org/customers/", "csv");