#!/usr/bin/env bash

# Deletes all printers in PaperCut that match a specific regular expression
# Use with care!
# Works on Mac and Linux (or Cygwin on Windows)

REGEX=${1:-'..*'}  # Provide a default that matches all printer names

if [[ $(( $(server-command list-printers | grep "$REGEX" | wc -l ) )) == 0 ]] ; then
  echo "No printers match \"$1\"."
else
  server-command list-printers | grep "$REGEX"

  echo
  read -p "About to delete this list of printers. Are you sure? [N/y] " -r < /dev/tty

  if [[ $REPLY =~ ^[Yy]$ ]] ; then
    server-command list-printers | grep mcx | while read -r x ; do server-command delete-printer  ${x%%\\*} ${x##*\\} ; done
  fi
fi


