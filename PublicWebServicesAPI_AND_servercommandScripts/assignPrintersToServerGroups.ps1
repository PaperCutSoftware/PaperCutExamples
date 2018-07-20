# Assign each printer to a group that corresponds to the print server name

# Developed by Matt Grant <mgrant@xrx.com.au>

#Declare $result as array

$result = @()

#Iterator for loop

$n = 0

#Query to retrieve list of printers. Drops the template printer and devices. Replaces \ with space

$parameters = 'list-printers | Out-String -Stream |Select-String -Pattern "^((?!!!|device).)*$" | ForEach-Object {$_ -Replace "\\"," "}'

#Run the command and put it in $result


# $result = Invoke-Expression "& '/Applications/PaperCut MF/server/bin/mac/server-command' $parameters"

$result = Invoke-Expression "& 'C:\Program Files\PaperCut MF\server\bin\win\server-command.exe' $parameters"



#iterate through each line in the array

foreach ($line in $result) {

  #splits the output so that the first word is put into $server and the consequent string is put into $queue

  $server,$queue = ($result[$n] -split ' ',2)

  #Removes -ps from the servername, this is only required for my customer as all the server names are like c30-ps.

  #Comment out or change as required

  $printergroup =($server -split '-')[0]

  #Handy for debugging

  $Output = "Adding printer group: $printergroup to Queue: $queue on server: $server"

  $Output

  #Run the command that adds the printer group to the printer

  # Invoke-Expression "& '/Applications/PaperCut MF/server/bin/mac/server-command' add-printer-group $server '$queue' $printergroup"

  Invoke-Expression "& 'C:\Program Files\PaperCut MF\server\bin\win\server-command.exe' add-printer-group $server '$queue' $printergroup"

  #iterate through the array

  $n = $n + 1

}