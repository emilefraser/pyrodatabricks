dbutils.library.install("dbfs:/path/to/your/library.whl")
dbutils.library.restartPython() # Removes Python state, but some libraries might not work without calling this command.