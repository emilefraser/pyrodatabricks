Function Invoke-DatabricksApiRequest {
	param 
	(	
        [Parameter(Mandatory = $true)] [string] [ValidateSet("DEFAULT", "DELETE", "GET", "HEAD", "MERGE",
                                                            "OPTIONS", "PATCH", "POST", "PUT", "TRACE")] $method,
        [Parameter(Mandatory = $true)] [string] $apiEndpoint,
        [Parameter(Mandatory = $true)] [string] $location,
		[Parameter(Mandatory = $true)] [string] $aadToken,
		[Parameter(Mandatory = $true)] [string] $azToken,
        [Parameter(Mandatory = $true)] [string] $wsId,
		[Parameter(Mandatory = $true)] $parameters
    )
    
    $apiUrl = "https://{0}.azuredatabricks.net/api/2.0/{1}" -f ($location, $apiEndpoint)
	
	$headers = @{
        'Authorization' = 'Bearer {0}'-f ($aadToken)
        'Content-Type' = 'application/json'
		'Accept' = 'application/json'
		'X-Databricks-Azure-SP-Management-Token' = $azToken
        'X-Databricks-Azure-Workspace-Resource-Id' = $wsId
    }
	
	if ($method -eq "GET") {	
		Write-Verbose "Body: `n$($body | Out-String)"
	}
	else {
		$body = ConvertTo-Json -InputObject $parameters
		Write-Host $body
	}
		
	$retry = 0
	do 
	{
		try {
			$result = Invoke-RestMethod -Uri $apiUrl -Method $method -Headers $headers -Body $body | ConvertTo-Json
			break
		} 
		catch {
			$retry += 1
			if($retry -le $script:dbApiCallRetryCount)
			{
				Write-Warning $_.Exception
				Write-Warning $_
				Write-Information "Retrying API call ($retry of $($script:dbApiCallRetryCount) retries) ..."
				Start-Sleep -Seconds $script:dbApiCallRetryWait
			}
			else
			{
				Write-Error  $_
			}
		}				
	}
	while($retry -le $script:dbApiCallRetryCount)	
	return $result
}

Function Get-Settings()
{
	Pop-Location
	Pop-Location
	Push-Location $($MyInvocation.InvocationName | Split-Path)
	Push-Location settings

	$global:BaseConfig = "./db_config.json"

	try {
		$global:Config = Get-Content "$BaseConfig" -Raw -ErrorAction:SilentlyContinue -WarningAction:SilentlyContinue | `
															ConvertFrom-Json -ErrorAction:SilentlyContinue -WarningAction:SilentlyContinue
	} catch {
		Write-Host -Message "The Base configuration file is missing!" -Stop
	}

	if (!($Config)) {
		Write-Host -Message "The Base configuration file is missing!" -Stop
	}

	return $Config
}