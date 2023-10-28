#!/bin/bash

job_id="${1}"
output=$(databricks jobs get --job-id="${job_code}" --output=JSON)
echo $output | jq

