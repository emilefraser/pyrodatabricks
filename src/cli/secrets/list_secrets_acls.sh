#!/bin/bash
echo "listing secret acls"
scopes=$(databricks secrets list-scopes --output=JSON)
scope_names=$(echo "$scopes" | jq -r '.scopes[] | [ .name ] | @tsv')
for scope_name in $scope_names
do
        echo "acls for scope: $scope_name"
        output=$(databricks secrets list-acls --scope="${scope_name}" --output=JSON)
        echo "${output}" | jq
done
echo "done"