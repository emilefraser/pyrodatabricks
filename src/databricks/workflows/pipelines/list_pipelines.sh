#!/bin/bash

pipelines=$(databricks pipelines list)
output=$(echo $pipelines | jq '.[] | {"pipeline_id":.pipeline_id, "name":.name}')
echo "${output}" | jq
