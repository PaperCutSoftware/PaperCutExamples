#!/usr/bin/env python3

# If a user is configured to auto charge to a single shared account then provide the account balance

# Because of a bug the current API users may ONLY have access to the single shared account they are using for this to work

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

shared_accounts = proxy.api.listUserSharedAccounts(auth, user, 0, 99, True)

if len(shared_accounts) == 1:
    print("User {} automatically charges to shared account \"{}\" which has a of balance {}".format(user, shared_accounts[0],
                                                   proxy.api.getSharedAccountAccountBalance(auth, shared_accounts[0])))
    exit(0)
elif len(shared_accounts) == 0:
    print("User {} has no access to a shared account. Cannot display balance".format(user))
else:
    print("User {} has access to more than one shared account. Cannot display balance".format(user))

exit(-1)

