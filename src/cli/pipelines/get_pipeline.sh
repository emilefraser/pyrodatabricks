#!/bin/bash

pipeline_id=${1}
output=$(databricks pipelines get --pipeline-id="${pipeline_id}")
echo "${output}" | jq
