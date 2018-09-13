#!/usr/bin/env python3

# Find all the users in a specific department

import xmlrpc.client
from ssl import create_default_context, Purpose
import sys

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

if len(sys.argv) != 2:
    print("No department name provided")
    sys.exit(1)

deptOfInterest = sys.argv[1]  # The dept of interest

offset = 0

limit = 100 # Max number of usernames to retrieve on each call

while True:
    try:
        userList = proxy.api.listUserAccounts(auth, offset,limit)
        # print("Got user list {}".format(userList))
    except xmlrpc.client.Fault as error:
        print("\ncalled listUserAccounts(). Return fault is {}".format(error.faultString))
        sys.exit(1)
    except xmlrpc.client.ProtocolError as error:
        print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
            error.url, error.headers, error.errcode, error.errmsg))
        sys.exit(1)

    for user in userList:
        try:
            dept = proxy.api.getUserProperty(auth, user, "department")  # Get the user's department
            # print("Got dept name \"{}\" for user {}".format(dept, user))
        except xmlrpc.client.Fault as error:
            print("\ncalled getUserProperty(). Return fault is {}".format(error.faultString))
            sys.exit(1)
        except xmlrpc.client.ProtocolError as error:
            print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                error.url, error.headers, error.errcode, error.errmsg))
            sys.exit(1)

        if dept ==  deptOfInterest:
            # Call your admin process here
            print("process user {} (dept {})".format(user, dept))

    if len(userList) < limit:
        break # We have reached the end

    offset += limit # We need to next slice of users

