# Report some simple PaperCut MF/NF information using the health API

# Setup and use the PaperCut web services API. More information at
# https://www.papercut.com/kb/Main/AdministeringPaperCutWithPowerShell
Add-Type -Path "$env:USERPROFILE\.nuget\packages\kveer.xmlrpc\1.1.1\lib\netstandard2.0\Kveer.XmlRPC.dll"
Add-Type -Path "$PWD\ServerCommandProxy\bin\Release\netstandard2.0\ServerCommandProxy.dll"

# Create a proxy object so we can call web services API XML-RPC methods
$s = New-Object PaperCut.ServerCommandProxy("localhost",9191,"token")

# Find the value of the Auth key in the PaperCut MF/NG config database
$authString = $s.GetConfigValue("health.api.key") 

# Set up the http header for the health API 
$headers = @{'Authorization' = $authString}

$uri = [Uri]"http://localhost:9191/api/health"

# Generate the report
&{
  # Get a list of the processes running 
  Get-Service -DisplayName  *PaperCut* | Select-Object -Property name,status  |
            ConvertTo-Html -Fragment -PreContent '<h2>PaperCut Processes</h2>'


  $rsp = Invoke-RestMethod -Uri $uri -Method Get -Headers $headers


#  $rsp.applicationServer.systemInfo |
#  ConvertTo-Html -As List -Fragment -PreContent '<h2>PaperCut Services Info</h2>'

  $rsp.license.devices | ConvertTo-Html -As List -Fragment -PreContent '<h2>License Info</h2>'
# $rsp.devices | ConvertTo-Html -As List -Fragment -PreContent '<h2>Device Info</h2>'


#  Write-Output "<p>Total Printers = $($rsp.printers.count)</p>"
#  Write-Output "<p>Total Devices = $($rsp.devices.count)</p>"
 } | Out-File -FilePath .\report1.html


Invoke-Expression .\report1.html
