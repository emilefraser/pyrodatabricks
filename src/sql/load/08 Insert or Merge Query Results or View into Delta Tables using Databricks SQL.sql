SHOW DATABASES;

USE lms_silver; SHOW TABLES;

USE lms_bronze; SHOW TABLES;

CREATE DATABASE IF NOT EXISTS lms_silver;

DROP TABLE IF EXISTS lms_silver.instructors;
CREATE TABLE IF NOT EXISTS lms_silver.instructors (
    instructor_id INT,
    instructor_name STRING,
    bl_created_ts TIMESTAMP,
    sl_updated_ts TIMESTAMP
);

DROP TABLE IF EXISTS lms_bronze.course_catalog;
CREATE TABLE IF NOT EXISTS lms_bronze.course_catalog (
    table_name STRING,
    record STRING,
    bl_created_ts TIMESTAMP
);

SELECT input_file_name(), table_name, record
FROM JSON.`dbfs:/FileStore/lms_dl/course_catalog` AS course_catalog;

COPY INTO lms_bronze.course_catalog
FROM (
    SELECT table_name,
        record,
        current_timestamp AS bl_created_ts
    FROM 'dbfs:/FileStore/lms_dl/course_catalog'
) FILEFORMAT = JSON
FILES = ('part-00000.json')
COPY_OPTIONS ('force' = 'true');

SELECT * FROM lms_bronze.course_catalog;

INSERT INTO lms_silver.instructors
SELECT record.*,
    bl_created_ts,
    current_timestamp AS sl_updated_ts
FROM (
    SELECT from_json(record, 'struct<instructor_id:INT, instructor_name:STRING>') AS record,
        bl_created_ts
    FROM lms_bronze.course_catalog
    WHERE table_name = 'instructors'
);

SELECT * FROM lms_silver.instructors;

SELECT input_file_name(), table_name, record
FROM JSON.`dbfs:/FileStore/lms_dl/course_catalog` AS course_catalog;

COPY INTO lms_bronze.course_catalog
FROM (
    SELECT table_name,
        record,
        current_timestamp AS bl_created_ts
    FROM 'dbfs:/FileStore/lms_dl/course_catalog'
) FILEFORMAT = JSON
FILES = ('part-00001.json');

SELECT * 
FROM lms_bronze.course_catalog
WHERE table_name = 'instructors'
ORDER BY bl_created_ts;

SELECT max(bl_created_ts) FROM lms_bronze.course_catalog;

SELECT record.*,
    bl_created_ts
FROM (
    SELECT from_json(record, 'struct<instructor_id:INT, instructor_name:STRING>') AS record,
        bl_created_ts
    FROM lms_bronze.course_catalog
    WHERE table_name = 'instructors'
        AND bl_created_ts >= (SELECT max(bl_created_ts) FROM lms_bronze.course_catalog)
);

            
SELECT * FROM lms_bronze.course_catalog
WHERE table_name = 'courses'
ORDER BY bl_created_ts;