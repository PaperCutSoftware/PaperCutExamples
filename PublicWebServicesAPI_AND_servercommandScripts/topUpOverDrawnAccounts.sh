#!/usr/bin/env bash

# Find all users with a negative balance and top up there account to zero.
# Normally you would expect to get funds from an external payment provider

# Note: This is for illustrative purposes only. In production we would recommend
# using the web services API for this type of payment feature.

# Instead of toppingup the account you may care to send the user
# a reminder to top up their payment purse as soon as possible. Remember
# you cant get a user's email address with the user properties call.

SERVER_COMMAND=~papercut/server/bin/mac/server-command

"${SERVER_COMMAND}" list-user-accounts | while read user ; do
  balance=$("${SERVER_COMMAND}" get-user-property $user balance)
  if [[ $balance < 0 ]] ; then
    # Might need to add a check to see if the user needs to be topped up.
    # Perhaps by checking group membership via get-user-groups or
    # by checking user's overdraft via get-user-property.

    # Should request funds from external source here
    topUp=$(echo "$balance * -1" | bc -q) # make it positive
    echo $user has -ve balance $balance about to top up user account with value $topUp
    "${SERVER_COMMAND}" adjust-user-account-balance $user $topUp "Remove -ve Balance"
  fi
done

