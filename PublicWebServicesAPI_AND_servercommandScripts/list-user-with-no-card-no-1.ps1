#!/usr/bin/env pwsh

# Lists all user accounts in PaperCut were the primary card ID is blank

# $SERVER_COMMAND = 'C:\Program Files\PaperCut MF\server\bin\win\server-command.exe'
$SERVER_COMMAND = '/Applications/PaperCut MF/server/bin/mac/server-command'

& $SERVER_COMMAND list-user-accounts | ForEach-Object {
    $cardNumber = & $SERVER_COMMAND get-user-property $_ primary-card-number
    if ( ! $cardNumber ) {
      Out-Host -InputObject $_
    }
}

