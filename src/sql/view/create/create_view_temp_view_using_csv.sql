-- mode "FAILFAST" will abort file parsing with a RuntimeException if any malformed lines are encountered
CREATE OR REPLACE TEMPORARY VIEW temp_delays USING CSV OPTIONS (
  path = '${DA.paths.datasets}/flights/departuredelays.csv',
  header = "true",
  mode = "FAILFAST" -- abort file parsing with a RuntimeException if any malformed lines are encountered
);