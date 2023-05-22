#!/bin/bash

echo "getting info for all clusters-policies"
clusterpolicies=$(databricks cluster-policies list --output JSON)
clusterpolicy_ids=$(echo $clusterpolicies | jq  -r '.policies[].policy_id')
for clusterpolicy_id in $clusterpolicy_ids
do   
    echo "CLUSTER-POLICIES with policy-id=${clusterpolicy_id}"
    output=$(databricks cluster-policies get --policy-id="${clusterpolicy_id}")
    echo $output | jq
done

