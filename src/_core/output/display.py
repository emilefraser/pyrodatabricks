# display shows the value in tabular format
# The display() command has the following capabilities and limitations:
#       Preview of results limited to 1000 records
#       Provides button to download results data as CSV
#       Allows rendering plots
path = f"{DA.paths.datasets}"
files = dbutils.fs.ls(path)
display(files)

# Out
# | path                    | name      | size  | modificationTime | 
# | dbfs:/mnt/dbacademy.... | ecommerce | 0     | 1678549190000 |
# ...
