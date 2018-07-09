#!/usr/bin/env bash

# Add each printer to a specific group based on the server attached to

# if you are using Windows then you can create a Powershell equivalent..

# Note if printers are moved the group membership can be updated via the user interface


# A simple PaperCut server script can do this. The process is as follows.

# 1) list all printers
# 2) Remove the template printer and all the devices from the lsit
# 3) Replace the '\' with a space
# 4) For each server printer run the add-printer-group command

# e.g. Using Linux or MacOS

server-command list-printers | egrep -v '^(!!)|(device)' | tr "\\" " " | while read server printer ; do
            server-command add-printer-group $server $printer "Server:$server"
done

