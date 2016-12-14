#!/usr/bin/env python3

# If a user is configured to auto charge to a single shared account then provide the account balance


import xmlrpc.client
import sys

host="http://localhost:9191/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth="password"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

if len(sys.argv) != 2:
    print("No user name supplied")
    exit(-1)

user=sys.argv[1]

proxy = xmlrpc.client.ServerProxy(host)

if not proxy.api.isUserExists(auth, user):
    print("Can't find user {}".format(user))
    exit(-1)

if  proxy.api.getUserProperty(auth,user, "account-selection.mode") != "AUTO_CHARGE_TO_SHARED":
    print("User {} is not configured to automatically charge to a shared account".format(user))
    exit(-1)

shared_account = proxy.api.getUserProperty(auth, user, "auto-shared-account")

if len(shared_account) == 0:
    print("Zero length account name returned")
    exit(-1)

print("User {} automatically charges to shared account \"{}\" which has a of balance {}".format(user, shared_account,
                                                   proxy.api.getSharedAccountAccountBalance(auth, shared_account)))

