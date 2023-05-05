#!/bin/bash

cluster_code="${1}"

output=$(databricks libraries cluster-status --cluster-id="${cluster_code}") || output=$(databricks libraries cluster-status --cluster-name="${cluster_code}")
echo $output | jq

