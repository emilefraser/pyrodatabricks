-- { { [CREATE OR] REPLACE TABLE | CREATE TABLE [ IF NOT EXISTS ] }
--   table_name
--   [ table_specification ] [ USING data_source ]
--   [ table_clauses ]
--   [ AS query ] }

-- table_specification
--   ( { column_identifier column_type [ NOT NULL ]
--       [ GENERATED ALWAYS AS ( expr ) |
--         GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( [ START WITH start ] [ INCREMENT BY step ] ) ] |
--         DEFAULT default_expression ]
--       [ COMMENT column_comment ]
--       [ column_constraint ] } [, ...]
--     [ , table_constraint ] [...] )

-- table_clauses
--   { OPTIONS clause |
--     PARTITIONED BY clause |
--     clustered_by_clause |
--     LOCATION path [ WITH ( CREDENTIAL credential_name ) ] |
--     COMMENT table_comment |
--     TBLPROPERTIES clause } [...]

-- clustered_by_clause
--   { CLUSTERED BY ( cluster_column [, ...] )
--     [ SORTED BY ( { sort_column [ ASC | DESC ] } [, ...] ) ]
--     INTO num_buckets BUCKETS }

-- data_source
--  Has to be one of: TEXT, AVRO, BINARYFILE, CSV, JSON, PARQUET, ORC, DELTA 
--  Other Options are JDBC and LIBSVM or fully qualified class name custom implementation org.apache.spark.sql.sources.DataSourceRegister

-- default
--   literatls, sql functions or operators except (aggregation, analyticsal, ranking, generators or subqueries)
--   supported only for csv, json, parquet and orc

-- GENERATED
--    either calculated column or identity

-- table_name
--    cannot include temporal specification

-- LOCATION path
--   Literal, specifying a location makes table an external tble. No location specified means its a managed table.
