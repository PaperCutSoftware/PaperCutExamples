#!/usr/bin/env pwsh

# Use PowerShell shell

# 1. Discover the latest PaperCut MF release version fron the Atom f  eed
# 2. Discover what version of PaperCut MF we are running
# 3. If they are not the same then create a job ticket, but only if we have not seen this release before


$MF_HOST = "$(hostname).local" # Modify to suit
$LAST_VERSION_CHECKED = "0.0.0" # Default to never checked
$PRODUCT = "mf" # Changing to "ng" should work, but has not been tested
$API_TOKEN = (Get-Content -raw ~/.PAPERCUT_API_TOKEN).trim()  # Don't hard code API tokens

if (Test-Path -Path ~/.PAPERCUT_LAST_VERSION_CHECKED ) {
  $LAST_VERSION_CHECKED = Get-Content ~/.PAPERCUT_LAST_VERSION_CHECKED
}

$CURRENT_RELEASE = ((Invoke-RestMethod -uri http://www.papercut.com/products/mf/release-history.atom).id  -replace "^tag:papercut.com,[0-9]+-[0-9]+-[0-9]+:$PRODUCT\/releases\/v(\d+)-(\d+)-(\d+)",'$1.$2.$3' | %{[System.Version]$_} | Sort-Object -Descending | Select-Object -first 1 ).toString()

Set-Content -Value $CURRENT_RELEASE -Path ~/.PAPERCUT_LAST_VERSION_CHECKED

if ( "$LAST_VERSION_CHECKED" -eq "$CURRENT_RELEASE" ) {
  Write-Host No new release
#  exit 0
}

# Assume we are on the PaperCut MF server and use server-command (NB Need to run in elevated shell for this to work)

if ( Test-Path -Path "$((Get-ItemProperty -Path 'HKLM:\HKEY_LOCAL_MACHINE\SOFTWARE\PaperCut MF').InstallPath)\server\bin\win\server-command.exe" ) {
  $HEALTH_API_KEY = `
    & "$((Get-ItemProperty -Path 'HKLM:\HKEY_LOCAL_MACHINE\SOFTWARE\PaperCut MF').InstallPath)\server\bin\win\server-command.exe" `
         get-config "health.api.key"

} else {

  $uri = [Uri] "http://${MF_HOST}:9191/rpc/api/xmlrpc"

  $HEALTH_API_KEY = (@"
<?xml version="1.0"?>
<methodCall>                 
<methodName>api.getConfigValue</methodName>
<params> 
<param>      
<value>${API_TOKEN}</value>                                                                                        
</param>
<param>
<value>health.api.key</value>
</param>
</params>
</methodCall>
"@ | Invoke-RestMethod  -Method 'Post' -Uri $uri | Select-Xml -XPath "/methodResponse/params/param/value").toString()

}

# Set up the http header for the health API 
$headers = @{'Authorization' = $HEALTH_API_KEY}

$uri = [Uri]"http://${MF_HOST}:9191/api/health"

$rsp = Invoke-RestMethod -Uri $uri -Method Get -Headers $headers

$INSTALLED_RELEASE = $rsp.applicationServer.systemInfo.Version -replace '^([\.\d]+).+','$1'

Write-Host Installed release is $INSTALLED_RELEASE

if ( "$INSTALLED_RELEASE" -eq  "$CURRENT_RELEASE" ) {
  Write-Host No new release, $INSTALLED_RELEASE is up to date
#  exit 0
}
