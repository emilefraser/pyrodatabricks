-- Composes a result set from one or more table references. 
-- The SELECT clause can be part of a query which also includes common table expressions (CTE), set operations, and various other clauses.

-- Delta lake guarantees:
-- that read against table will always return most recent version of table
-- will never encounter a state of deadlock due to ongoing operation (no conflicting operations)
SELECT [ hints ] [ ALL | DISTINCT ] { named_expression | star_clause } [, ...]
  FROM table_reference [, ...]
  [ LATERAL VIEW clause ]
  [ WHERE clause ]
  [ GROUP BY clause ]
  [ HAVING clause]
  [ QUALIFY clause ]

named_expression
   expression [ column_alias ]

star_clause
   [ { table_name | view_name } . ] * [ except_clause ]

except_clause
   EXCEPT ( { column_name | field_name } [, ...] )