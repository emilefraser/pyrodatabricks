#!/bin/bash

source_path="${1}"
target_path="${2}"

# list the dbfs dbfs
databricks fs mv "{$source_path}" "{$target_path}"