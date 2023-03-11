#! /usr/bin/pwsh
Function Add-SecretsScope($aadToken, $azToken, $wsId, $scopeName, $location)
{
    . ".\General.ps1"

    $parameters = @{
        'scope' = $scopeName
        'initial_manage_principal' = 'users'
    }

    $apiEndpoint = "secrets/scopes/create"
    Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters
}

Function Add-SecretsToScope($aadToken, $azToken, $wsId, $location, $scopeName, $armOutputs)
{
    . ".\General.ps1"

    $keys = $armOutputs | ConvertFrom-Json
    $keys.PSObject.Properties | ForEach-Object {
        $type = ($_.Value.type).ToLower()
        $key = $_.Name
        $value = $_.Value.value

        $parameters = @{
            'scope' =  $scopeName
            'key' = $key
            'string_value' = $value
        }

        $apiEndpoint = "secrets/put"
        Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                    -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters
    }
}