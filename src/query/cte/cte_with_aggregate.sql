WITH lax_bos AS (
  WITH origin_destination (origin_airport, destination_airport) AS (
    SELECT
      origin,
      destination
    FROM
      external_table
  )
  SELECT
    *
  FROM
    origin_destination
  WHERE
    origin_airport = 'LAX'
    AND destination_airport = 'BOS'
)
SELECT
  count(origin_airport) AS `Total Flights from LAX to BOS`
FROM
  lax_bos;