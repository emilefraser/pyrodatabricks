#!/bin/bash

output=$(databricks clusters list --output=JSON)
echo $output | jq '[ .clusters[] | { cluster_id: .cluster_id, cluster_name: .cluster_name } ]'



