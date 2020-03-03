# For dll set-up see
# https://www.papercut.com/kb/Main/AdministeringPaperCutWithPowerShell

# Set a path to the required libraries
$ libPath = 'C:\code\lib'

#Import them
Add-Type -Path “$libPath\ServerCommandProxy.dll”
Add-Type -Path “$libPath\CookComputing.XmlRpcV2.dll”

# Connect to the PaperCut Server
$s = New-Object PaperCut.ServerCommandProxy(“localhost”,9191,”password”);

# Initialise and array for fetching users from the PaperCut server
$userArray = New-Object string[] 0;

# Execute the following loop, retrieving batches of users 100 at a time until less than 100 is returned (indicating the end of PaperCut's users)
$intCounter = 0;
do{
    
    #Get the next (up to) 100 users
    $userArray = $s.ListUserAccounts($intCounter, 100);
    
    # Loop through each user
    foreach($user in $userArray)
    {
        # Get their card numbers
        $primaryCardNumber = $s.GetUserProperty($user, 'primary-card-number');
        $secondaryCardNumber = $s.GetUserProperty($user, 'secondary-card-number');
        
        Write-Host "Swapping Primary ($primaryCardNumber) and Secondary ($secondaryCardNumber) card numbers for $user"
        
        # Set them to their alternate places
        $s.SetUserProperty($user, 'primary-card-number',$secondaryCardNumber);
        $s.SetUserProperty($user, 'secondary-card-number',$primaryCardNumber);
    }
    
    # Need the 100 users
    $intCounter += 100;
    
}while($userArray.length -eq 100)

# We're done

