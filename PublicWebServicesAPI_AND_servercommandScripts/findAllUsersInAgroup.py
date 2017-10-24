#!/usr/bin/env python3


import xmlrpc.client
import sys

host="http://localhost:9191/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host)

if len(sys.argv) != 2:
    print("No group name provided")
    sys.exit(1)

group = sys.argv[1]

offset = 0

limit = 100

while True:
    try:
        userList = proxy.api.listUserAccounts(auth, offset,limit)
        # print("Got user list {}".format(userList))
    except xmlrpc.client.Fault as error:
        print("\ncalled userExit with incorrect args. Return fault is {}".format(error.faultString))
        sys.exit(1)
    except xmlrpc.client.ProtocolError as error:
        print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
            error.url, error.headers, error.errcode, error.errmsg))
        sys.exit(1)

    for user in userList:
        try:
            groups = proxy.api.getUserGroups(auth, user)
            # print("Got group list {} for user {}".format(groups, user))
        except xmlrpc.client.Fault as error:
            print("\ncalled userExit with incorrect args. Return fault is {}".format(error.faultString))
            sys.exit(1)
        except xmlrpc.client.ProtocolError as error:
            print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                error.url, error.headers, error.errcode, error.errmsg))
            sys.exit(1)

        if group in groups:
            # Call you admin process here
            print("process user {}".format(user))

    if len(userList) < limit:
        break # We have reached the end

    offset += limit # We need to next slice of users

