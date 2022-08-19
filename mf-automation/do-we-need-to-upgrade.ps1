#!/usr/bin/env pwsh

# 1. Discover the latest PaperCut MF release version fron the Atom webste feed
# 2. Discover what version of PaperCut MF we are running
# 3. If they are not the same then create a job ticket, but only if we have not seen this release before

# PaperCut version are in semver format, which PowerShell supports via the .NET System.Version type

$MF_HOST = "$(hostname).local" # Modify to suit
$PRODUCT = "mf" # Changing to "ng" should work, but has not been tested
$GH_REPO = "PaperCutSoftware/PaperCutExamples"
$MINION = "alecthegeek" # Assignee for review tickets

$HEALTH_API_KEY = ""

# Assume we are on the PaperCut MF server and use server-command (NB Need to run in elevated shell for this to work)
$HEALTH_API_KEY = `
    & "$((Get-ItemProperty -Path 'HKLM:\HKEY_LOCAL_MACHINE\SOFTWARE\PaperCut MF').InstallPath)\server\bin\win\server-command.exe" `
         get-config "health.api.key"

if ($LASTEXITCODE -ne 0 ) {

  # Server command did not work. Use the web services API

  # Need a web services API token.Get this from your local PaperCut admin 
  $API_TOKEN = (Get-Content -raw ~/.PAPERCUT_API_TOKEN).trim()  # Don't hard code API tokens

  $HEALTH_API_KEY = (@"
<?xml version="1.0"?>
<methodCall>                 
<methodName>api.getConfigValue</methodName>
<params> 
<param>      
<value>$API_TOKEN</value>                                                                                        
</param>
<param>
<value>health.api.key</value>
</param>
</params>
</methodCall>
"@ | Invoke-RestMethod  -Method 'Post' -Uri "http://${MF_HOST}:9191/rpc/api/xmlrpc" | Select-Xml -XPath "/methodResponse/params/param/value").toString()


}

if ($HEALTH_API_KEY.Length -eq 0 )
{
  Write-Host Could not retrieve health API key
  Exit-PSHostProcess 1
}

$URI = [Uri]"http://${MF_HOST}:9191/api/health"

$rsp = Invoke-RestMethod -Uri $URI -Method Get -Headers @{ 'Authorization' = $HEALTH_API_KEY }

$INSTALLED_RELEASE = [System.Version]($rsp.applicationServer.systemInfo.Version -replace '^([\.\d]+).+','$1')

# Get the latest release from the PaperCut website (parse the XML Atom feed)
$CURRENT_RELEASE = [System.Version]((Invoke-RestMethod -uri http://www.papercut.com/products/mf/release-history.atom).id[0]  `
        -replace "^tag:papercut.com,[0-9]+-[0-9]+-[0-9]+:$PRODUCT\/releases\/v(\d+)-(\d+)-(\d+)",'$1.$2.$3')

Write-Host "Latest PaperCut release is $CURRENT_RELEASE. Installed Release is $INSTALLED_RELEASE"

try {
  $LAST_VERSION_CHECKED = Import-Clixml -path ~/LAST_VERSION_CHECKED 
}
catch {
  $LAST_VERSION_CHECKED = $INSTALLED_RELEASE
}

if ( "$LAST_VERSION_CHECKED" -eq "$CURRENT_RELEASE" ) {
  Write-Host PaperCut $PRODUCT_UPCASE $CURRENT_RELEASE  already checked. Nothing to do here
  Exit-PSHostProcess 0
}

if ( "$CURRENT_RELEASE"  -eq  "$INSTALLED_RELEASE") {
  Write-Host Installed release $INSTALLED_RELEASE is already up to date. No new update available 
  Exit-PSHostProcess 0
}

Write-Host PaperCut $PRODUCT.ToUpper() $INSTALLED_RELEASE.ToString() can be upgraded to $CURRENT_RELEASE.ToString()

$RELEASE_NOTES="https://www.papercut.com/products/$PRODUCT/release-history/$($CURRENT_RELEASE.MAJOR)-$($CURRENT_RELEASE.MINOR)/#v$($CURRENT_RELEASE.MAJOR)-$($CURRENT_RELEASE.MINOR)-$($CURRENT_RELEASE.BUILD)"

# Use appropriate API for your ticket system
$env:GH_TOKEN = (Get-Content -raw ~/.GITHUB_ACCESS_TOKEN).trim()

gh issue -R "$GH_REPO" create -a "$MINION" `
  -t "Review PaperCut $($PRODUCT.ToUpper()) $($INSTALLED_RELEASE.ToString()) upgrade to version $($CURRENT_RELEASE.ToString())" `
  -b "Review release notes at $RELEASE_NOTES"

Export-Clixml -path ~/LAST_VERSION_CHECKED -InputObject $CURRENT_RELEASE
