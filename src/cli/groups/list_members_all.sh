#!/bin/bash

echo "Retrieving all members in all groups"
groups=$(databricks groups list)
group_names=$(echo $groups | jq -r '.group_names | @tsv')
for group_name in $group_names
do
		echo "Retrieving members in the group ${group_name}"
        members=$(databricks groups list-members --group-name=${group_name})
        echo "${members}" | jq
done
echo "Done"
