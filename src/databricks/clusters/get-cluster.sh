#!/bin/bash

cluster_code="${1}"
output=$(databricks clusters get --cluster-id="${cluster_code}" --output=JSON) || output=$(databricks clusters get --cluster-name="${cluster_code}" --output=JSON)
echo $output | jq

