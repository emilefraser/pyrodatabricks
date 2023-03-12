CREATE OR REPLACE TABLE delta.`/tmp/delta/people10m` (
  id INT,
  firstName STRING,
  middleName STRING,
  lastName STRING,
  salary INT
) USING DELTA