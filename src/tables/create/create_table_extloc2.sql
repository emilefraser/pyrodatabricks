-- Creates delta table from external directory (UNMANAGED)
CREATE TABLE student (
	id integer,
	name string
	)
USING DELTA LOCATION '/mnt/path_to_empty_location';
