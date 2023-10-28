#!/bin/bash

echo "getting all libraries for all clusters"
output=$(databricks libraries all-cluster-statuses)
echo "${output}" | jq
