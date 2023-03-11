-- CreTe table and specify table comment and properties
CREATE TABLE student (
	id INT, 
	name STRING, 
	age INT
	)
    COMMENT 'this is a comment'
    TBLPROPERTIES ('foo'='bar');
