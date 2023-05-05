#!/bin/bash
echo "getting all runs"
runs=$(databricks repos list)
run_ids=$(echo "${runs}" | jq -r '.runs[] | [.run_id] | @tsv')
for run_id in $run_ids
do
        echo "getting run info for run_id:${run_id}" 
        output=$(databricks runs get --run-id="${run_id}")
        echo "${output}" | jq
done
echo "done"
