#!/bin/bash

repo_code="${1}"
output=$(databricks repos get --repo-id="${repo_code}") || output=$(databricks repos get --path="${repo_code}")
echo $output | jq
