-- Only for Databricks Runtime 11.3+
INSERT INTO students 
PARTITION (student_id = 444444)
SELECT 
    name, 
    address 
FROM 
    persons 
WHERE 
    name = "Dora Williams";