MERGE INTO lms_silver.users AS lsu
USING lms_bronze.users AS lbu
ON lsu.user_id = lbu.user_id
    WHEN MATCHED AND lbu.last_op = 'U' THEN
        UPDATE SET *
    WHEN MATCHED AND lbu.last_op = 'D' THEN
        DELETE
    WHEN NOT MATCHED THEN
        INSERT *;