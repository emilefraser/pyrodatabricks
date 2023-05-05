#!/bin/bash

output=$(databricks libraries list | jq '.statuses[] | { "cluster_id":.cluster_id,"library_path":.library_statuses[].library | .[] }')
echo $output | jq
