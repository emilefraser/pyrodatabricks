#!/bin/bash
echo "listing secret scopes"
scopes=$(databricks secrets list-scopes --output=JSON)
output=$(echo $scopes | jq '.scopes[] | { "name": .name, "backend_type": .backend_type}')
echo "${output}" | jq
echo "done"