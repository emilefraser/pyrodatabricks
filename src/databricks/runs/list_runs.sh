#!/bin/bash
echo "listing job runs"
output=$(databricks runs list)
echo $output | jq
echo "done"
