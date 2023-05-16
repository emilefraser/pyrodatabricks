-- Create a table with a generated column
CREATE TABLE rectangles(
	a INT,
	b INT, 
	area INT GENERATED ALWAYS AS (a * b)
	);