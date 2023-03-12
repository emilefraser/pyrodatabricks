-- Create partitioned table
CREATE TABLE student (
	id INT, 
	name STRING, 
	age INT
)
PARTITIONED BY (
    age
);