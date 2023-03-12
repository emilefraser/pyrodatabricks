-- Inserts new rows into a table and optionally truncates the table or partitions. 

-- You specify the inserted rows by value expressions or the result of a query.

-- Databricks SQL supports this statement only for Delta Lake Tables

-- When you INSERT INTO a Delta table, schema enforcement and evolution is supported. 
--  If a column’s data type cannot be safely cast to a Delta table’s data type, a runtime exception is thrown. 

-- No "COMMIT" keyword

INSERT { OVERWRITE | INTO } [ TABLE ] table_name
    [ PARTITION clause ]
    [ ( column_name [, ...] ) ]
    query

INSERT INTO [ TABLE ] table_name
    REPLACE WHERE predicate
    query


-- OUT
-- num_affected_rows | num_inserted_rows