#!/bin/bash

echo "listing all instance-pools"
output=$(databricks instance-pools list)
echo "${output}" | jq
echo "done"