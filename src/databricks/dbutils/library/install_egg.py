dbutils.library.install("dbfs:/path/to/your/library.egg")
dbutils.library.restartPython() # Removes Python state, but some libraries might not work without calling this  command.