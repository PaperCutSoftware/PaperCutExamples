#!/bin/sh

# Swaps the contents of primary and secondary card numbers in the database

# Sometimes (after you've loaded all the card numbers in PaperCut) you need
# to interface into an external system that requires all the card numbers to
# be swapped between the primary and secondary fields in the PaperCut database,

# Here is a handy script

server-command list-user-accounts | while read x;do
  primary=$(server-command get-user-property $x "secondary-card-number")
  secondary=$(server-command get-user-property $x "primary-card-number")
  server-command set-user-property $x "primary-card-number" "$primary"
  server-command set-user-property $x "secondary-card-number" "$secondary"
done

