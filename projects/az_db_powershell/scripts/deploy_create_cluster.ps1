#! /usr/bin/pwsh
Function Add-Cluster($aadToken, $azToken, $wsId, $clusterName, $sparkVersion, $nodeType, $numWorkers, $location)
{
    . ".\General.ps1"

    $parameters = @{
        'cluster_name' = $clusterName
        'spark_version' = $sparkVersion
        'node_type_id' = $nodeType
        'spark_conf' = @{
            'spark.speculation' = 'true'
        }
        'num_workers' = $numWorkers
    }

    $apiEndpoint = "clusters/create"
    Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters
}