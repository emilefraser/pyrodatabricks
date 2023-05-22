CREATE OR REFRESH STREAMING TABLE table_name;

APPLY CHANGES INTO LIVE.table_name
FROM source
KEYS (keys)
[WHERE condition]
[IGNORE NULL UPDATES]
[APPLY AS DELETE WHEN condition]
[APPLY AS TRUNCATE WHEN condition]
SEQUENCE BY orderByColumn
[COLUMNS {columnList | * EXCEPT (exceptColumnList)}]
[STORED AS {SCD TYPE 1 | SCD TYPE 2}]
[TRACK HISTORY ON {columnList | * EXCEPT (exceptColumnList)}]