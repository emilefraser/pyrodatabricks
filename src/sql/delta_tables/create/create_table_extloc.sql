-- Creates delta table from external directory (UNMANAGED)
CREATE TABLE student 
USING DELTA LOCATION '/mnt/path_to_existing_location';
