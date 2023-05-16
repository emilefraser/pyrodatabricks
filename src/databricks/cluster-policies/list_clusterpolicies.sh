#!/bin/bash

output=$(databricks cluster-policies list --output=JSON)
echo $output | jq

