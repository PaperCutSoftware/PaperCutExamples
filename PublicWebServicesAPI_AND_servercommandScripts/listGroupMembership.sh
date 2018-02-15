#!/usr/bin/env bash


server-command list-user-accounts | xargs -I {} echo 'printf "%s:\t%s\n" {} : $(server-command get-user-groups {})'|bash


