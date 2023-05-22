-- Create filled table from another table (managed)
-- CTAS
CREATE TABLE student_copy 
AS 
SELECT 
	* 
FROM 
	student;
