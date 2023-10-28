#!/bin/bash

echo "getting info for all jobs"
output=$(databricks jobs list --output=JSON | jq '[ .jobs ]')
echo $output | jq
