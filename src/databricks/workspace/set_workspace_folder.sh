#!/bin/bash

folders="${1}"
echo "creating folders: ${folders}"
databricks mkdirs "${folders}"
echo "completed successfully"

