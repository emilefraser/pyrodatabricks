# The Python code below demonstrates parsing the table properties field, filtering those options that are specifically geared toward controlling Delta Lake behavior. In this case, logic could be written to further parse these properties to identify all tables in a database that contain PII.
def parse_table_keys(database, table=None):
    table_keys = {}
    if table:
        query = f"SHOW TABLES IN {DA.db_name} LIKE '{table}'"
    else:
        query = f"SHOW TABLES IN {DA.db_name}"
    for table_item in spark.sql(query).collect():
        table_name = table_item[1]
        key_values = spark.sql(f"DESCRIBE EXTENDED {DA.db_name}.{table_name}").filter("col_name = 'Table Properties'").collect()[0][1][1:-1].split(",")
        table_keys[table_name] = [kv for kv in key_values if not kv.startswith("delta.")]
    return table_keys

parse_table_keys(DA.db_name)   