#! /usr/bin/pwsh
Function Invoke-DatabricksFSFile($aadToken, $azToken, $wsId, $location, $dbfsPath, $localPathSettings, `
                            $overWrite, $batchSize = 1048000)
{
    . ".\General.ps1"

    $dbfsFile = Add-DatabricksFSFile -aadToken $aadToken -azToken $azToken -wsId $wsId -location $location `
									-dbfsPath $dbfsPath -overWrite $overWrite
	$dbfsFile = $dbfsFile | Convertfrom-json
	
	Write-Host "Reading content from $localPathSettings ..."
	$localFile = [System.IO.File]::ReadAllBytes($localPathSettings)
	$totalSize = $localFile.Length
	
	Write-Host "Starting upload of file in batches of size $batchSize ..."
	$offset = 0
	do
	{
		Write-Host "Adding new content from offset $offset ..."
		if($offset + $batchSize -gt $totalSize)
		{
			$batchSize = $totalSize - $offset
		}
		$content = $localFile[$offset..$($offset + $batchSize)]
		$contentB64 = [System.Convert]::ToBase64String($content)
		
        Add-DatabricksFSFileBlock -aadToken $aadToken -azToken $azToken -wsId $wsId -location $location `
                                -handle $dbfsFile.handle -data $contentB64
		
		$offset = $offset + $batchSize + 1
	}
	while($offset -lt $totalSize)
	Write-Host "Finished uploading local file '$localPathSettings' to DBFS '$dbfsPath'"
	
	Close-DatabricksFSFile -aadToken $aadToken -azToken $azToken -wsId $wsId -location $location -handle $dbfsFile.handle
	
	return $dbfsPath
}

Function Add-DatabricksFSFile($aadToken, $azToken, $wsId, $location, $dbfsPath, $overWrite)
{
    . ".\General.ps1"

	$apiEndpoint = "dbfs/create"

	$parameters = @{
		path = $dbfsPath 
		overwrite = $overWrite 
	}
	
	$result = Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters

	return $result
}

Function Add-DatabricksFSFileBlock($aadToken, $azToken, $wsId, $location, $handle, $data, $AsPlainText)
{
    . ".\General.ps1"

	$apiEndpoint = "dbfs/add-block"

	if($AsPlainText)
	{
		$data = $data | ConvertTo-Base64 -Encoding ([Text.Encoding]::UTF8)
	}
	
	$parameters = @{
		handle = $handle 
		data = $data 
	}
	
	$result = Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters

	return $result
}

Function Add-DatabricksFSDirectory($aadToken, $azToken, $wsId, $location, $dbfsPath)
{
    . ".\General.ps1"

	$apiEndpoint = "dbfs/mkdirs"

	$parameters = @{
		path = $dbfsPath 
	}
	
	$result = Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters

	return $result
}

Function Remove-DatabricksFSDirectory($aadToken, $azToken, $wsId, $location, $dbfsPath)
{
    . ".\General.ps1"

	$apiEndpoint = "dbfs/delete"

	$parameters = @{
		path = $dbfsPath 
	}
	
	$result = Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters

	return $result
}

Function Close-DatabricksFSFile($aadToken, $azToken, $wsId, $location, $handle)
{
	$apiEndpoint = "dbfs/close"

	$parameters = @{
		handle = $handle 
	}
	
	$result = Invoke-DatabricksApiRequest -Method "Post" -apiEndpoint $apiEndpoint -location $location `
                                -aadToken $aadToken -azToken $azToken -wsId $wsId -parameters $parameters

	return $result
}