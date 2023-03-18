CREATE OR REPLACE VIEW BOS_LAX 
AS WITH origin_destination(origin_airport, destination_airport) 
AS (SELECT origin, destination FROM external_table)
SELECT * FROM origin_destination
WHERE origin_airport = 'BOS' AND destination_airport = 'LAX';

SELECT count(origin_airport) AS `Number of Delayed Flights from BOS to LAX` FROM BOS_LAX;