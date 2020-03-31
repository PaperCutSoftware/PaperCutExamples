#!/usr/bin/env python3

import xmlrpc.client
from ssl import create_default_context, Purpose
import sys

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut
auth="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

offset = 0

limit = 100 # Max number of usernames to retrieve on each call

while True:
    try:
        userList = proxy.api.listUserAccounts(auth, offset,limit)
    except xmlrpc.client.Fault as error:
        print("\ncalled listUserAccounts(). Return fault is {}".format(error.faultString))
        sys.exit(1)
    except xmlrpc.client.ProtocolError as error:
        print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\n" +
                "Error code: {}\nError message: {}".format(
            error.url, error.headers, error.errcode, error.errmsg))
        sys.exit(1)
    except ConnectionRefusedError as error:
        print("Connection refused. Is the Papercut server running?")
        sys.exit(1)

    for user in userList:
        try:
            primary = proxy.api.getUserProperty(auth, user, "secondary-card-number")
            secondary = proxy.api.getUserProperty(auth, user, "primary-card-number")
            proxy.api.setUserProperty(auth, user, "primary-card-number", primary)
            proxy.api.setUserProperty(auth, user, "secondary-card-number", secondary)

        except:
            print("\nSomething went wrong. Return fault is {}".format(sys.exc_info()[0]))
            sys.exit(1)

    if len(userList) < limit:
        break # We have reached the end

    offset += limit # We need to next slice of users
