#!/bin/bash

file_name="https://azstgcdatprdsan01.blob.core.windows.net/databricks/dbc/other/notebooks.dbc?sv=2021-10-04&st=2023-03-05T23%3A23%3A13Z&se=2023-03-06T23%3A23%3A13Z&sr=b&sp=r&sig=07dZ9Jr17j3fNP%2BYG7v8AUEnE9x5SMBDu2Ed1eyVe4g%3D"
workspace_name="/Users/efraser25@gmail.com/notebooks"

# databricks workspace import s"<local-path-where-exports-live>" "<databricks-target-path>"
databricks workspace import "${file_name}" "${workspace_name}" --format="DBC" --language="PYTHON"
