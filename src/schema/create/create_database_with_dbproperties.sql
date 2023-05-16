CREATE DATABASE IF NOT EXISTS ${da.db_name}
COMMENT "This is a test database"
LOCATION "${da.paths.user_db}"
WITH DBPROPERTIES (contains_pii = true)