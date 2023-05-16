#!/bin/bash

group_name="${1}"
echo "Retrieving all members in group ${group_name}"
members=$(databricks groups list-members --group-name=${group_name})
echo "${members}" | jq
echo "Done"
