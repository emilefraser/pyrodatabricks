#!/bin/bash

file_name="src/dbc/other/"
workspace_name="/Users/efraser25@gmail.com/other"

# databricks workspace import s"<local-path-where-exports-live>" "<databricks-target-path>"
databricks workspace import_dir "${file_name}" "${workspace_name}"