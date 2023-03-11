#! /usr/bin/pwsh
Function Add-Token($wsId, $location, $aadToken, $azToken)
{   
    . ".\General.ps1"

    $parameters = @{
        'lifetime_seconds' = -1
        "comment" = "auto-generated token"
    }

    $apiEndpoint = "token/create"

    $response = Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                            -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters
    $b = $response | Convertfrom-json
    $token_value = $b.token_value
    $token_id = $b.token_info.token_id

    return $token_value, $token_id
}