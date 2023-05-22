CREATE LIVE TABLE nyctaxi_raw
COMMENT "This is the raw nyctaxi dataset in Delta Format."
SELECT * FROM delta. `/mnt/raw/delta/Factnyctaxi`
 
CREATE LIVE TABLE Factnyctaxi_staging(
  CONSTRAINT valid_VendorID EXPECT (VendorID IS NOT NULL),
  CONSTRAINT valid_passenger_count EXPECT (passenger_count > 0) ON VIOLATION DROP ROW
)
COMMENT "nyctaxi data cleaned and prepared for analysis."
AS SELECT
  VendorID AS ID,
  CAST(passenger_count AS INT) AS Count,
  total_amount AS Amount,
  trip_distance AS Distance,
  tpep_pickup_datetime AS PickUp_Datetime,
  tpep_dropoff_datetime AS DropOff_Datetime
FROM live.nyctaxi_raw
 
 
CREATE LIVE TABLE Factnyctaxi
COMMENT "The curated Factnyc table containing aggregated counts, amounts, and distance data."
AS SELECT
  VendorID AS ID,
  tpep_pickup_datetime AS PickUp_Datetime,
  tpep_dropoff_datetime AS DropOff_Datetime,
  CAST(passenger_count AS INT) AS Count,
  total_amount AS Amount,
  trip_distance AS Distance
FROM live.Factnyctaxi_staging
WHERE tpep_pickup_datetime BETWEEN '2019-03-01 00:00:00' AND  '2020-03-01 00:00:00'
AND passenger_count IS NOT NULL
GROUP BY VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, CAST(passenger_count AS INT), total_amount, trip_distance
ORDER BY VendorID ASC