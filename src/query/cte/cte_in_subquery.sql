SELECT
  max(total_delay) AS `Longest Delay (in minutes)`
FROM
  (
    WITH delayed_flights(total_delay) AS (
      SELECT
        delay
      FROM
        external_table
    )
    SELECT
      *
    FROM
      delayed_flights
  );