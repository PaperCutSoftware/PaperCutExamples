#!/usr/bin/env bash

server-command list-user-accounts | while read -r u ; do
  if [[ $(server-command get-user-property $u ${1:?'Must supply user property name'}) == "${2:?'Must supply value to match'}" ]] ; then
      echo $u
      # Might want to exit here on 1st match
  fi
done

