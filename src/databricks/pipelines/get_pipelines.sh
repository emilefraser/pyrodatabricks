#!/bin/bash

pipelines=$(databricks pipelines list)
pipeline_ids=$(echo $pipelines | jq -r '.[] | [.pipeline_id] | @tsv')
for pipeline_id in $pipeline_ids
do
        output=$(databricks pipelines get --pipeline-id="${pipeline_id}")
        echo $output | jq
done
