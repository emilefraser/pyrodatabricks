#!/bin/bash

file_name="src/dbc/other/notebooks.dbc"
workspace_name="/Users/efraser25@gmail.com/notebooks"

# databricks workspace import s"<local-path-where-exports-live>" "<databricks-target-path>"
databricks workspace import "${file_name}" "${workspace_name}" --format="DBC" --language="PYTHON"