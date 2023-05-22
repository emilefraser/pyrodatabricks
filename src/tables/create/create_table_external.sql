CREATE TABLE IF NOT EXISTS ${da.db_name}.pii_test_2
(id INT, name STRING COMMENT "PII")
COMMENT "Contains PII"
LOCATION "${da.paths.working_dir}/pii_test_2"
TBLPROPERTIES ('contains_pii' = True) 