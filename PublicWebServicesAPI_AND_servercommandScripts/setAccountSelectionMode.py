#!/usr/bin/env python3

# For every user in the database, set the account selection mode to be either

# 1. Auto charge to personal when user has access to zero shared accounts
# 2. Auto charge to shared account when user has access to one shared account
# 3. User standard account selection pop up when user has access to multiple shared accounts

# This script would need to be run regularly to reflect group changes etc

import xmlrpc.client
from ssl import create_default_context, Purpose

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut
auth="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

offset = 0

limit = 100 # Max number of usernames to retrieve on each call

while True:

  userList = proxy.api.listUserAccounts(auth, offset,limit)

  for user in userList:

    if not proxy.api.isUserExists(auth, user):
      print("Can't find user {}".format(user))

    shared_accounts = proxy.api.listUserSharedAccounts(auth, user, 0, 99, True)

    if len(shared_accounts) == 0:
      proxy.api.setUserAccountSelectionAutoChargePersonal(auth, user, False)
      print("Setting setUserAccountSelectionAutoChargePersonal for user {}".format(user))

    elif len(shared_accounts) == 1:
      proxy.api.setUserAccountSelectionAutoSelectSharedAccount(auth, user, shared_accounts[0], False)
      print("Setting setUserAccountSelectionAutoSelectSharedAccount for user {} with account {}".format(
                                      user, shared_accounts[0]))

    else:
      proxy.api.setUserAccountSelectionStandardPopup(auth, user, False, True, False, False, False)
      print("Setting setUserAccountSelectionStandardPopup for user {}".format(user))

  if len(userList) < limit:
    break # We have reached the end

  offset += limit # We need to next slice of users

