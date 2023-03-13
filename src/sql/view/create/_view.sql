-- Constructs a virtual table that has no physical data based on the result-set of a SQL query. 
-- ALTER VIEW and DROP VIEW only change metadata.


CREATE [ OR REPLACE ] [ TEMPORARY ] VIEW [ IF NOT EXISTS ] view_name
    [ column_list ]
    [ COMMENT view_comment ]
    [ TBLPROPERTIES clause ]
    AS query

column_list
   ( { column_alias [ COMMENT column_comment ] } [, ...] )