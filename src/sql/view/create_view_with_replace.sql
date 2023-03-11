CREATE OR REPLACE VIEW view_name (
    id COMMENT 'Unique identification number', 
    name
)
COMMENT 'Bronze layer'
AS
  SELECT 
    id, 
    name
  FROM 
  VALUES (0, "zero"), (1, "one") t(id, name)