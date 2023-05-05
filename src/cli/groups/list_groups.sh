#!/bin/bash

output=$(databricks groups list)
echo "${output}" | jq

