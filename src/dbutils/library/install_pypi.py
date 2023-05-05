dbutils.library.installPyPI("pypipackage", version="version", repo="repo", extras="extras")
dbutils.library.restartPython()  # Removes Python state, but some libraries might not work without calling this command.

dbutils.library.installPyPI("torch")
dbutils.library.installPyPI("scikit-learn", version="1.19.1")
dbutils.library.installPyPI("azureml-sdk", extras="databricks")
dbutils.library.restartPython() # Removes Python state, but some libraries might not work without calling this command.