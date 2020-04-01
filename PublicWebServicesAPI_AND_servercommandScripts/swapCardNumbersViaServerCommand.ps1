
Function server-command {
    &'C:\Program Files\PaperCut MF\server\bin\win\server-command.exe' $Args
}

server-command list-user-accounts | ForEach-Object {
  $primary=(server-command get-user-property $_ "secondary-card-number")
  $secondary=(server-command get-user-property $_ "primary-card-number")
  server-command set-user-property $_ "primary-card-number" "$primary"
  server-command set-user-property $_ "secondary-card-number" "$secondary"
}

