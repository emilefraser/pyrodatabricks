#!/bin/bash
echo "getting all repos"
repos=$(databricks repos list)
repo_ids=$(echo $repos | jq -r '.repos[] | [.id] | @tsv')
for repo_id in $repo_ids
do
        echo "getting repo info for repo_id:${repo_id}" 
        output=$(databricks repos get --repo-id="${repo_id}")
        echo $output | jq
done
echo "done"
