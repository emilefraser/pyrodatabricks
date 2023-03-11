#! /usr/bin/pwsh
Function Import-DatabricksWorkspaceItem($aadToken, $azToken, $wsId, $location, $wsFilePath, `
                                        $format, $language, $localPath, $overwrite)
{
    . ".\General.ps1"

    Write-Host "Reading content from $localPath ..."
    $fileBytes = [IO.File]::ReadAllBytes($localPath)
    Write-Host "Converting content to Base64 string ..."
    $content = [Convert]::ToBase64String($fileBytes)

    $parameters = @{
        'path' = $wsFilePath
        'format' = $format
        'language' = $language
        'content' = $content
    }

    $apiEndpoint = "workspace/import"
    Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters
}

Function Add-DatabricksWorkspaceDirectory($aadToken, $azToken, $wsId, $location, $wsPath)
{
    . ".\General.ps1"

    $parameters = @{
        'path' = $wsPath
    }

    $apiEndpoint = "workspace/mkdirs"
    Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -wsId $wsId -parameters $parameters
}