#!/bin/bash

run_id="${1}"
echo "getting job run info for run: ${run_id}"
output=$(databricks runs get --run_id="${run_id}")
echo "${output}" | jq


