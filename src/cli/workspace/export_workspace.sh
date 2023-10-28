#!/bin/bash
# The general template is databricks workspace export_dir "<databricks-source-path>" "<local-path-to-export-to>"
if [ -n "${1}" ]
then
    export_folder="${1}"
else
    export_folder="./"
fi 

echo "exporting workspace to folder: ${export_folder}"
# exports entire workspace to export folder
databricks workspace export_dir "/" "${export_folder}" -o
echo "done"
