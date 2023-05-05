#!/bin/bash

output=$(databricks jobs list --output=JSON | jq '[ .jobs[] | { job_id: .job_id, job_name: .job_name } ]')
echo $output | jq
