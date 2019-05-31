#!/usr/bin/env python3

# Find all the users in a specific user group
# via the server command
# available in 19.1.0 onwards

import xmlrpc.client
from ssl import create_default_context, Purpose
import sys

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then the client address will need to be whitelisted in PaperCut

auth="secret"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

#proxy = xmlrpc.client.ServerProxy(host, verbose=True, transport=xmlrpc.client.SafeTransport, context=ctx)
proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

#This is how we can retrieve list of users of a group, prior to 19.1.0"
def oldMethod(groupName, offset, limit):
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

        print("\n" + groupName + " members (prior to 19.1.0 version):")
                
        for user in userList:
            try:
                groups = proxy.api.getUserGroups(auth, user)  # Get a list of groups for the current user of interest
                if(groupName.strip('!!') in g for g in groups or "All Users".lower() in groupName.lower()):            
                    print(user)
            except xmlrpc.client.Fault as error:
                print("\ncalled getUserGroups(). Return fault is {}".format(error.faultString))
                sys.exit(1)
            except xmlrpc.client.ProtocolError as error:
                print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                    error.url, error.headers, error.errcode, error.errmsg))
                sys.exit(1)

            if group in groups:
                # Call your admin process here
                print("process user {} (group {})".format(user, group))

        if len(userList) < limit:
            break # We have reached the end

        offset += limit # We need to next slice of users


def newMethod(groupName, offset, limit):
    try:
        userList = proxy.api.getGroupMembers(auth, group, offset, limit)
        print("\n" + groupName + " members (19.1.0 version and above):")
        for user in userList:
            print(user)
    except Exception as e:
        print(e)

if __name__=="__main__":
    if len(sys.argv) != 2:
        print("No group name provided")
        sys.exit(1)

    group = sys.argv[1]  # The user group of interest

    offset = 0

    limit = 100 # Max number of usernames to retrieve on each call

        
    oldMethod(group, offset, limit)
    newMethod(group, offset, limit)
