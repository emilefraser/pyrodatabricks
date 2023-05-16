-- DESC or DESCRIBE
DESCRIBE EXTENDED dbname.table

-- MANAGED
/*
| col_name                     | data_type                                                             | comment |
|------------------------------|-----------------------------------------------------------------------|---------|
| id                           | int                                                                   | null    |
| name                         | string                                                                | PII     |
|                              |                                                                       |         |
| # Detailed Table Information |                                                                       |         |
| Catalog                      | spark_catalog                                                         |         |
| Database                     | dbacademy_efraser25_gmail_com_adewd_1_1                               |         |
| Table                        | pii_test                                                              |         |
| Type                         | MANAGED                                                               |         |
| Comment                      | Contains PII                                                          |         |
| Location                     | dbfs:/user/efraser25@gmail.com/dbacademy/adewd/1.1/1_1.db/pii_test    |         |
| Provider                     | delta                                                                 |         |
| Owner                        | root                                                                  |         |
| Is_managed_location          | TRUE                                                                  |         |
| Table Properties             | [contains_pii=true,delta.minReaderVersion=1,delta.minWriterVersion=2] |         |
*/

-- UNMANAGED/EXTERNAL
/*
| col_name                     | data_type                                                             |
|------------------------------|-----------------------------------------------------------------------|
| id                           | int                                                                   |
| name                         | string                                                                |
|                              |                                                                       |
| # Detailed Table Information |                                                                       |
| Catalog                      | spark_catalog                                                         |
| Database                     | dbacademy_efraser25_gmail_com_adewd_1_1                               |
| Table                        | pii_test_2                                                            |
| Type                         | EXTERNAL                                                              |
| Comment                      | Contains PII                                                          |
| Location                     | dbfs:/user/efraser25@gmail.com/dbacademy/adewd/1.1/pii_test_2         |
| Provider                     | delta                                                                 |
| Owner                        | root                                                                  |
| Table Properties             | [contains_pii=true,delta.minReaderVersion=1,delta.minWriterVersion=2] |
*/