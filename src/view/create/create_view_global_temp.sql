-- Global temp views behave much like other temporary views but differ in one important way.
-- eThey are added to the global_temp database that exists on the cluster.
CREATE OR REPLACE GLOBAL TEMP VIEW gv_race_results
AS
SELECT *
  FROM demo.race_results_python
  WHERE race_year = 2012