df = spark.read.load(f"{DA.paths.datasets}/nyctaxi-with-zipcodes/data")
display(df)

# out[0]
# {{tablular version of the data}}