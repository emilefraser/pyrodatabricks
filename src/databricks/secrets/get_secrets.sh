#!/bin/bash

scope_name="${1}"

echo "getting secrets for scope ${scope_name}"
output=$(databricks secrets list --scope="${scope_name}" --output=JSON)
echo "${output}" | jq
echo "done"