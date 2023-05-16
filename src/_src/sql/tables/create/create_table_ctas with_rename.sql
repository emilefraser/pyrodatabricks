-- Create filled table from another table (managed)
-- CTAS
CREATE TABLE student_copy 
AS 
SELECT 
	id AS student_id
,	student_name
,	marks AS percentage_quarter
FROM 
	student;
