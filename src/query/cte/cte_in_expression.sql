SELECT
  (
    WITH distinct_origins AS (
      SELECT DISTINCT origin FROM external_table
    )
    SELECT
      count(origin) AS `Number of Distinct Origins`
    FROM
      distinct_origins
  ) AS `Number of Different Origin Airports`;