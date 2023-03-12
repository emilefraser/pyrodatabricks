-- Creates delta table with explicit format (MANAGED)
-- Explicit format is only needed for versions prior to DB Runtime 8.0
CREATE TABLE student USING DELTA;