CREATE TABLE demo.race_results_sql
AS
SELECT *
  FROM demo.race_results_python
  WHERE race_year = 2020