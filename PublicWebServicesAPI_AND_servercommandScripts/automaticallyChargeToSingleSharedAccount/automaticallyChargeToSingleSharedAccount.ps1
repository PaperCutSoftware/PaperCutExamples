# Navigate to the location of the server-command executable. 
# For more information on server-command, see https://www.papercut.com/help/manuals/ng-mf/common/tools-server-command/
cd "C:\Program Files\PaperCut MF\server\bin\win"

# Set the location of the CSV file contain the user to shared account mappings.
$data = Import-CSV -Path C:\users\installer\desktop\set-account-data.csv -Delimiter ";"

# We will run through each record in the CSV and set the user to 'Automatically charge to a single shared account' and assign the relevant account. 
$data | ForEach {

    $user = $_.username
    $account = $_.account

    # Set Shared shared account for user
    Invoke-Expression "& 'C:\Program Files\PaperCut MF\server\bin\win\server-command.exe' set-user-account-selection-auto-select-shared-account $user $account FALSE"
}
