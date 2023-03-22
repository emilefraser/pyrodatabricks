CREATE OR REFRESH STREAMING TABLE table_name
AS SELECT *
  FROM cloud_files(
    "<file_path>",
    "<file_format>",
    map(
      "<option_key>", "<option_value",
      "<option_key>", "<option_value",
      ...
    )
  )