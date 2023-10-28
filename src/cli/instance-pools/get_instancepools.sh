#!/bin/bash

echo "getting info for all instance pools"
output=$(databricks instance-pool list --output JSON | jq '[ .pool[] ]')
echo "${output}" | jq
echo "done"