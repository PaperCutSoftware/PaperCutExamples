# For dll set-up see
# https://www.papercut.com/kb/Main/AdministeringPaperCutWithPowerShell

#Import the dlls we need
Add-Type -Path "$env:USERPROFILE\.nuget\packages\kveer.xmlrpc\1.1.1\lib\netstandard2.0\Kveer.XmlRPC.dll"
Add-Type -Path "$PWD\ServerCommandProxy\bin\Release\netstandard2.0\ServerCommandProxy.dll"

$papercuthost = "localhost" # If not localhost then this address will need to be whitelisted in PaperCut
$auth = "token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

# Proxy object to call PaperCut Server API
$s = New-Object PaperCut.ServerCommandProxy($papercuthost, 9191, $auth);

$BATCH_SIZE = 100

$(do {
    [array]$userList = $s.ListUserAccounts($intCounter, $BATCH_SIZE)
    Write-Output $userList
    $intCounter += $BATCH_SIZE
} while ($userList.Length -eq $BATCH_SIZE) ) | ForEach-Object {

        $cardNumbers = $s.GetUserProperties($_, @("secondary-card-number","primary-card-number"))
        $s.SetUserProperties($_, @(@("primary-card-number", $cardNumbers[0]), @("secondary-card-number", $cardNumbers[1])))
}
