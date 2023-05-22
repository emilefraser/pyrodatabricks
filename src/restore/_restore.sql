-- Restores a Delta table to an earlier state. Restoring to an earlier version number or a timestamp is supported.

RESTORE [ TABLE ] table_name [ TO ] time_travel_version

time_travel_version
 { TIMESTAMP AS OF timestamp_expression |
   VERSION AS OF version }

/*
| table_size_after_restore | num_of_files_after_restore | num_removed_files | num_restored_files | removed_files_size | restored_files_size |
|--------------------------|----------------------------|-------------------|--------------------|--------------------|---------------------|
| 1098                     | 1                          | 0                 | 1                  | 0                  | 1098                |
*/