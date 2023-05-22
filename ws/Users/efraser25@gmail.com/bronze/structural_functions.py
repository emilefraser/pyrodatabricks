# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Structural functions
# MAGIC
# MAGIC Contains the following funtions/methods to help with strutural changes
# MAGIC - Flatten the input to contain only simple types (tabular)
# MAGIC - Unflattening of structures
# MAGIC
# MAGIC This is esspecially for JSON and XML

# COMMAND ----------

from pyspark.sql import functions as f
from pyspark.sql import types as t

# COMMAND ----------

# dynamically flattens table and adds to dataframe
def flatten_json(df, 
            nest_separator = '__',
            replace_column_prefix = None,
            search_column_string = '.',
            replace_column_string = '_',
            root_keys_to_ignore = None
            ):

    complex_fields = dict([
        (field.name, field.dataType) 
        for field in df.schema.fields 
        if isinstance(field.dataType, t.ArrayType) or isinstance(field.dataType, t.StructType)
    ])
 
    qualify = list(complex_fields.keys())[0] + nest_separator

    while len(complex_fields) != 0:
        col_name = list(complex_fields.keys())[0]
        
        if isinstance(complex_fields[col_name], t.StructType):
            expanded = [f.col(col_name + '.' + '`' + k + '`').alias(qualify + k) 
                        for k in [ n.name for n in  complex_fields[col_name]]
                       ]
            df = df.select("*", *expanded).drop(col_name)
    
        elif isinstance(complex_fields[col_name], t.ArrayType): 
            df = df.withColumn(col_name, f.explode(col_name))
          
        complex_fields = dict([
            (field.name, field.dataType)
            for field in df.schema.fields
            if isinstance(field.dataType, t.ArrayType) or isinstance(field.dataType, t.StructType)
        ])
        
        
    df = df.toDF(*(c.replace(search_column_string, replace_column_string) for c in df.columns))
        
    return df