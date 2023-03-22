/*
The cloud_files() method enables Auto Loader to be used natively with SQL. This method takes the following positional parameters:

The source location, as mentioned above
The source data format, which is JSON in this case
An arbitrarily sized array of optional reader options. In this case, we set cloudFiles.inferColumnTypes to true
*/
CREATE OR REFRESH STREAMING LIVE TABLE sales_orders_raw
COMMENT "The raw sales orders, ingested from retail-org/sales_orders."
AS SELECT * FROM cloud_files("${datasets_path}/retail-org/sales_orders", "json", map("cloudFiles.inferColumnTypes", "true"))