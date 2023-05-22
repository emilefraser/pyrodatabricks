# Maintenance - Drop managed tables
This notebook will clean up the table space by dropping all managed tables, including the metadata and underlying data. This process is necessary when updating table schemas (e.g., changing data types).

***Note:*** *It is advised to backup your data first.*

## Recommended procedure
* Back-up data tables in ADLS (not implemented here)
* Run maintenance - drop managed tables notebook (this notebook)
* Re-import all data. 

## Technical details about Delta table operations
Deleting Delta tables is a very time-consuming operation because they contain a lot of metadata and transaction logs. According to [Best Practices for Dropping Managed Databricks Delta Tables](https://docs.databricks.com/user-guide/faq/drop-delta-table.html), `DELETE FROM` and `VACUUM` operations should be run before dropping a Delta table. This ensures that metadata and file sizes are cleaned up before initiating data deletion. These operations reduce the amount of metadata and number of uncommitted files that would increase deletion time.

Listing catalogue tables is also a costly operation. See [Listing Table Names](https://docs.databricks.com/user-guide/faq/list-tables.html) for more information.