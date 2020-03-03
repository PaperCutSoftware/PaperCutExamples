#!/usr/bin/env bash

# print a csv list of all the printers with the value of the printer property in $1.

# If $1 is not given defaults to the "disabled" propery

# For a list of possible properties see
# https://github.com/PaperCutSoftware/PaperCutExamples/wiki/Get-Set-Advanced-Printer-Properties


server-command list-printers |
  while IFS='\'  read -r s p ; do
    if [[ $s != '!!template printer!!'  &&  $s != "device"  ]] ; then
      echo \""$s\",\"$p\",\"$(server-command get-printer-property $s $p ${1:-disabled})\""
    fi
  done