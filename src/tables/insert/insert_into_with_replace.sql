-- Only for Databricks Runtime 12.0+
-- DELETES all values between the WHERE clauses
-- INSERT values as specified
-- Original values OUTSIDE WHERE clause left intact
INSERT INTO sales REPLACE WHERE tx_date BETWEEN '2022-10-01' AND '2022-10-31'
   VALUES (DATE'2022-10-01', 1237),
          (DATE'2022-10-02', 2378),
          (DATE'2022-10-04', 2456),
          (DATE'2022-10-05', 6328);