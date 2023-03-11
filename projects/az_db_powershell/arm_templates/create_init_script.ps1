param (
    [Parameter(Mandatory=$true)][string]$filePath,
    [Parameter(Mandatory=$true)][string]$armOutputString,
    [Parameter(Mandatory=$true)][string]$clientId,
    [Parameter(Mandatory=$true)][string]$secret
)

Function Invoke-Replace($content, $key, $value){
    return $content -Replace "$key = "".*?""", "$key = '$value'"
}

$content = Get-Content -Raw -Path $filePath

$armOutputObj = $armOutputString | ConvertFrom-Json

$armOutputObj.PSObject.Properties | ForEach-Object {
    $type = ($_.value.type).ToLower()
    $key = $_.name
    $value = $_.value.value
    $content = Invoke-Replace -content $content -key $key -value $value
}

$content = $content -Replace "clientId = "".*?""", "clientId = '$clientId'"
$content = $content -Replace "secret = "".*?""", "secret = '$secret'"

$content | Out-File $filePath
