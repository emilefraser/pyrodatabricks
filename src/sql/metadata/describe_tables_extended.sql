-- DESC or DESCRIBE
DESCRIBE EXTENDED dbname.table

/*
| col_name                     | data_type                                                                                           | comment |
|------------------------------|-----------------------------------------------------------------------------------------------------|---------|
| id                           | int                                                                                                 | null    |
| name                         | string                                                                                              | null    |
| value                        | double                                                                                              | null    |
|                              |                                                                                                     |         |
| # Detailed Table Information |                                                                                                     |         |
| Catalog                      | spark_catalog                                                                                       |         |
| Database                     | efraser25_y82l_da_dewd                                                                              |         |
| Table                        | students                                                                                            |         |
| Type                         | MANAGED                                                                                             |         |
| Location                     | dbfs:/mnt/dbacademy-users/efraser25@gmail.com/data-engineering-with-databricks/database.db/students |         |
| Provider                     | delta                                                                                               |         |
| Owner                        | root                                                                                                |         |
| Is_managed_location          | true                                                                                                |         |
| Table Properties             | [delta.minReaderVersion=1,delta.minWriterVersion=2]                                                 |         |
*/