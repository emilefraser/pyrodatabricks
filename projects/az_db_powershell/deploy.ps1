#! /usr/bin/pwsh
param (
    [parameter(Mandatory=$true)][string]$subscriptionId,
    [Parameter(Mandatory=$true)][string]$resourceGroupName,
    [Parameter(Mandatory=$true)][string]$tenantId,
    [Parameter(Mandatory=$true)][string]$location,
    [Parameter(Mandatory=$true)][string]$databricksWorkspace,
    [Parameter(Mandatory=$true)][string]$servicePrincipalId,
    [Parameter(Mandatory=$true)][string]$servicePrincipalPassword,
    [Parameter(Mandatory=$true)][string]$armOutputs,
    [Parameter(Mandatory=$true)][string]$dbLocalPathsDBFSSettings,
    [Parameter(Mandatory=$true)][string]$dbLocalPathsNotebooks,
    [Parameter(Mandatory=$true)][string]$dbLocalPathSharedFiles
)

Write-Host "Login in your account" -ForegroundColor Yellow
az login --service-principal --allow-no-subscriptions --username $servicePrincipalId `
        --password $servicePrincipalPassword --tenant $tenantId

az account set --subscription $subscriptionId

Push-Location $($MyInvocation.InvocationName | Split-Path)
Push-Location scripts

. ".\General.ps1"
$Config = Get-Settings
Write-Host $Config

Pop-Location
Pop-Location

$wsId = az resource show --resource-type "Microsoft.Databricks/workspaces" -g "$resourceGroupName" -n "$databricksWorkspace" --query id -o tsv

Get a token for the global Databricks application
$token_response = az account get-access-token --resource $Config.AZURE_GLOBAL_DATABRICKS_APPLICATION
$aadToken = $token_response | Convertfrom-json
Write-Host $aadToken.accessToken -ForegroundColor Yellow

Get a token for the Azure management API
$azToken_response = az account get-access-token --resource $Config.AZURE_MANAGEMENT_API
$azToken = $azToken_response | Convertfrom-json
Write-Host $azToken.accessToken -ForegroundColor Yellow

Push-Location $($MyInvocation.InvocationName | Split-Path)
Push-Location scripts

Write-Host "--------------------------------------------------------" -ForegroundColor Yellow
Write-Host "Creating Azure Databricks Token - $databricksWorkspace" -ForegroundColor Yellow
Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow

. ".\Deploy-Create-Token.ps1"
$token_value, $token_id = Add-Token -wsId $wsId -location $location -aadToken $aadToken.accessToken -azToken $azToken.accessToken
Write-Host $token_value $token_id

Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow
Write-Host "Creating Azure Databricks Cluster - $databricksWorkspace" -ForegroundColor Yellow
Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow

. ".\Deploy-Create-Cluster.ps1"
Add-Cluster -aadToken $aadToken.accessToken -azToken $azToken.accessToken -wsId $wsId -clusterName $Config.DATABRICKS_CLUSTER_NAME `
            -sparkVersion $Config.DATABRICKS_SPARK_VERSION -nodeType $Config.DATABRICKS_NODE_TYPE `
            -numWorkers $Config.DATABRICKS_NUM_WORKERS -location $location

Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow
Write-Host "Creating Azure Databricks Secrets - $databricksWorkspace" -ForegroundColor Yellow
Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow

. ".\Deploy-Create-Secrets.ps1"
Add-SecretsScope -aadToken $aadToken.accessToken -azToken $azToken.accessToken -wsId $wsId -scopeName $Config.DATABRICKS_SECRETS_SCOPE -location $location
Add-SecretsToScope -aadToken $aadToken.accessToken -azToken $azToken.accessToken -wsId $wsId -location $location `
                -scopeName $Config.DATABRICKS_SECRETS_SCOPE -armOutputs $armOutputs

Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow
Write-Host "Uploading Settings to DBFS - $databricksWorkspace" -ForegroundColor Yellow
Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow

. ".\Deploy-Create-DBFS.ps1"
$list = Get-ChildItem -Path $dbLocalPathsDBFSSettings
ForEach($n in $list){
    Write-Host $n.Name
    $dbfsPath = $Config.DATABRICKS_DBFS_PATH + $n.Name
    $localPathSettings = $dbLocalPathsDBFSSettings + $n.Name
    Invoke-DatabricksFSFile -aadToken $aadToken.accessToken -azToken $azToken.accessToken -wsId $wsId -location $location `
                    -dbfsPath $dbfsPath -localPathSettings $localPathSettings `
                    -overWrite $Config.DATABRICKS_FILE_OVERWRITE
}

Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow
Write-Host "Uploading Notebooks and Shared files to Azure Databricks Workspace - $databricksWorkspace" -ForegroundColor Yellow
Write-Host "-------------------------------------------------------- " -ForegroundColor Yellow
. ".\Deploy-Create-Workspace.ps1"

$list = Get-ChildItem -Path $dbLocalPathsNotebooks
ForEach($n in $list){
    Write-Host $n.Name
    $wsFilePath = $Config.DATABRICKS_WS_NOTEBOOKS_PATH + $n.Name
    $localPath = $dbLocalPathsNotebooks + $n.Name
    Import-DatabricksWorkspaceItem -aadToken $aadToken.accessToken -azToken $azToken.accessToken -wsId $wsId -location $location `
                                -wsFilePath $wsFilePath -format $Config.DATABRICKS_FILE_FORMAT `
                                -language $Config.DATABRICKS_FILE_LANGUAGE -localPath $localPath `
                                -overwrite $Config.DATABRICKS_FILE_OVERWRITE
}

$list = Get-ChildItem -Path $dbLocalPathSharedFiles
ForEach($n in $list){
    Write-Host $n.Name
    $wsFilePath = $Config.DATABRICKS_WS_SHARED + $n.Name
    $localPath = $dbLocalPathSharedFiles + $n.Name
    Import-DatabricksWorkspaceItem -aadToken $aadToken.accessToken -azToken $azToken.accessToken -wsId $wsId -location $location `
                                -wsFilePath $wsFilePath -format "SOURCE" `
                                -language $Config.DATABRICKS_FILE_LANGUAGE -localPath $localPath `
                                -overwrite $Config.DATABRICKS_FILE_OVERWRITE
}

Pop-Location
Pop-Location