# Deletes all user accounts in PaperCut that match a specific regular expression
# Use with care!

# Provide a default that matches all account names
param([String]$regex='.+')

$SERVER_COMMAND = 'C:\Program Files\PaperCut MF\server\bin\win\server-command.exe'

& $SERVER_COMMAND list-user-accounts | Where-Object {$_ -cmatch $regex} | Out-Host -Paging

if (Read-Host -Prompt 'About to delete this list of users. Are you sure? [N/y] ' | Where-Object {$_ -cmatch 'y' } ) {
  & $SERVER_COMMAND list-user-accounts | Where-Object {$_ -cmatch $regex} | ForEach-Object -Process {& $SERVER_COMMAND  delete-existing-user $_ }
}

