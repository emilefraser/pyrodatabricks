files = dbutils.fs.ls(f"{DA.paths.user_db}/bronze/_delta_log")
display(files)