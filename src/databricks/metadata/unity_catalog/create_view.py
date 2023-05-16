

CREATE VIEW < catalog_name >.< schema_name >.< view_name > as
SELECT
  id,
  CASE WHEN is_member(< group_name >) THEN email ELSE 'REDACTED' END AS email,
  country,
  product,
  total
FROM
  < catalog_name >.< schema_name >.< table_name >;
GRANT USE CATALOG ON CATALOG < catalog_name > TO < group_name >;
GRANT USE SCHEMA ON SCHEMA < catalog_name >.< schema_name >.< view_name >;
TO < group_name >;
GRANT
SELECT
  ON < catalog_name >.< schema_name >.< view_name >;
TO < group_name >;


CREATE VIEW < catalog_name >.< schema_name >.< view_name > as
SELECT
  *
FROM
  < catalog_name >.< schema_name >.< table_name >
WHERE
  CASE WHEN is_member(managers) THEN TRUE ELSE total <= 1000000 END;
GRANT USE CATALOG ON CATALOG < catalog_name > TO < group_name >;
GRANT USE SCHEMA ON SCHEMA < catalog_name >.< schema_name >.< table_name >;
TO < group_name >;
GRANT
SELECT
  ON < catalog_name >.< schema_name >.< table_name >;
TO < group_name >;