#!/bin/bash

file_name="${1}"

# list the dbfs dbfs
databricks fs mkdirs "{$file_name}"