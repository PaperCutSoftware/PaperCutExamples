#!/usr/bin/env pwsh
## Lists the current balance for all shared accounts
# Works with Windows Powershell


$SERVER_COMMAND = 'C:\Program Files\PaperCut MF\server\bin\win\server-command.exe'

& $SERVER_COMMAND list-shared-accounts | ForEach-Object  {
 $b = & $SERVER_COMMAND get-shared-account-account-balance $_
 Write-Output "$_`t`t$b"
}

