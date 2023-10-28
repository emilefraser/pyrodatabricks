#!/bin/bash

echo "getting info from all instance pools"
clusterpolicy_id="${1}"
output=$(databricks cluster-policies get --policy-id="${clusterpolicy_id}")
echo "${output}" | jq
echo "done"
