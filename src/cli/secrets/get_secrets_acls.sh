#!/bin/bash

scope_name="${1}"
principal_name="${2}"

echo "getting acls for scope ${scope_name}"
output=$(databricks secrets get-acl --scope="${scope_name}" --principal="${principal_name}" --output=JSON)
echo "${output}" | jq
echo "done"