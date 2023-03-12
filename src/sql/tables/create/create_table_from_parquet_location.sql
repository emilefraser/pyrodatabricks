CREATE TABLE IF NOT EXISTS db_name.student
(
	id integer,
	student_name string,
	final_mark int
)
USING PARQUET
LOCATION "/mnt/studentlake/marks"
