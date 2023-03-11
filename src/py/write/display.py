# display shows the value in tabular format
path = f"{DA.paths.datasets}"
files = dbutils.fs.ls(path)
display(files)