#!/bin/bash

echo "getting info for all clusters"
output=$(databricks clusters list --output JSON | jq '[ .clusters[] ]')
echo "${output}" | jq

#jobs=$(databricks jobs list)
#for job in $jobs
#do
#/    job_id=$(echo $jobs | cut -d ' ' -f 1)
 #   echo "job with job_id=${job_id}"
 #   output=$(databricks jobs get --job-id="${job_id}")
 #   echo $output | jq
#done

