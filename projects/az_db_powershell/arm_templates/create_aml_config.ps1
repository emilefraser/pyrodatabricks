param (
    [Parameter(Mandatory=$true)][string]$filePath,
    [Parameter(Mandatory=$true)][string]$armOutputString
)

$aml_config = Get-Content -Raw -Path $filePath | Convertfrom-json

$armOutputObj = $armOutputString | ConvertFrom-Json

$armOutputObj.PSObject.Properties | ForEach-Object {
    $type = ($_.value.type).ToLower()
    $key = $_.name
    $value = $_.value.value

    if ($key -eq "subscriptionId"){
        $aml_config.subscription_id = $value
    }elseif ($key -eq "resourceGroupName") {
        $aml_config.resource_group = $value
    }elseif ($key -eq "amlWorkspaceName") {
        $aml_config.workspace_name = $value
    }
}

Write-Host $aml_config

$aml_config | ConvertTo-Json | Out-File $filePath
