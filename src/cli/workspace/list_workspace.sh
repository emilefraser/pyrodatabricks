#!/bin/bash

output=$(databricks workspace list)
echo $output | jq

