display(dbutils.fs.ls(f"{DA.paths.user_db}/students"))

# or
files = dbutils.fs.ls(f"{DA.paths.user_db}/students")
display(files)