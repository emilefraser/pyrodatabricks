#!/bin/bash

clusterpolicy_id="${1}"
output=$(databricks cluster-policies get --policy-id="${clusterpolicy_id}")
echo $output | jq

