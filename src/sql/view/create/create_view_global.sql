CREATE OR REPLACE GLOBAL VIEW gv_race_results
AS
SELECT *
  FROM demo.race_results_python
  WHERE race_year = 2012