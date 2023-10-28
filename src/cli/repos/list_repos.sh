#!/bin/bash

repos=$(databricks repos list)
output=$(echo $repos | jq '.repos[] | {"id":.id,"path":.path,"url":.url}')
echo $output | jq
