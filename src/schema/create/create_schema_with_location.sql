-- Note schma created under dbfs:/user/hive/warehouse/
-- note schema directory is schema name with .db extension
CREATE SCHEMA IF NOT EXISTS ${da.schema_name}_custom_location LOCATION '${da.paths.working_dir}/_custom_location.db';