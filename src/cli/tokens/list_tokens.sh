#!/bin/bash
echo "listing tokens"
output=$(databricks tokens list)
echo "${output}" | jq
echo "done"