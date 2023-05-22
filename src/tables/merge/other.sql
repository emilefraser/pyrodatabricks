-- in[0]
-- description
SELECT
    *
FROM
    schema.table

--out[0]
/*

*/
WITH course_catalog_cte AS (
    SELECT record.*,
        bl_created_ts,
        current_timestamp AS sl_updated_ts
    FROM (
        SELECT from_json(record, 'struct<instructor_id:INT, instructor_name:STRING>') AS record,
            bl_created_ts
        FROM lms_bronze.course_catalog
        WHERE table_name = 'instructors'
            AND bl_created_ts >= (SELECT max(bl_created_ts) FROM lms_bronze.course_catalog)
    )
) SELECT * FROM course_catalog_cte;

WITH course_catalog_cte AS (
    SELECT record.*,
        bl_created_ts,
        current_timestamp AS sl_updated_ts
    FROM (
        SELECT from_json(record, 'struct<instructor_id:INT, instructor_name:STRING>') AS record,
            bl_created_ts
        FROM lms_bronze.course_catalog
        WHERE table_name = 'instructors'
            AND bl_created_ts >= (SELECT max(bl_created_ts) FROM lms_bronze.course_catalog)
    )
) MERGE INTO lms_silver.instructors AS i
    USING course_catalog_cte AS cc
        ON i.instructor_id = cc.instructor_id
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *;
    
SELECT * FROM lms_silver.instructors;

WITH course_catalog_cte AS (
    SELECT record.*,
        bl_created_ts,
        current_timestamp AS sl_updated_ts
    FROM (
        SELECT from_json(record, 'struct<instructor_id:INT, instructor_name:STRING>') AS record,
            bl_created_ts
        FROM lms_bronze.course_catalog
        WHERE table_name = 'instructors'
            AND bl_created_ts >= (SELECT max(bl_created_ts) FROM lms_bronze.course_catalog)
    )
) MERGE INTO lms_silver.instructors AS i
    USING course_catalog_cte AS cc
        ON i.instructor_id = cc.instructor_id
    WHEN MATCHED THEN 
        UPDATE SET
            i.instructor_name = cc.instructor_name,
            i.bl_created_ts = cc.bl_created_ts,
            i.sl_updated_ts = cc.sl_updated_ts
    WHEN NOT MATCHED THEN 
        INSERT 
            (instructor_id, instructor_name, bl_created_ts, sl_updated_ts)
        VALUES
            (cc.instructor_id, cc.instructor_name, cc.bl_created_ts, cc.sl_updated_ts);