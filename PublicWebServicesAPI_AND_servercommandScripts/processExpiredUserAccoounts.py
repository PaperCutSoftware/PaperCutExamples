#! /usr/bin/env python3

from xmlrpc import client as xmlrpcclient

from ssl import create_default_context, Purpose
from time import sleep
from sys import exit
from json import dumps, loads
from datetime import date, timedelta

host = "https://localhost:9192/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth = "token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

accountExpiry =  10 # No of days before an new account is deleted.

proxy = xmlrpcclient.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))


offset = 0

limit = 100 # Max number of usernames to retrieve on each call

while True:
    try:
        userList = proxy.api.getGroupMembers(auth, "!!Internal Users!!", offset,limit)
        # print("Got user list {}".format(userList))
    except xmlrpcclient.Fault as error:
        print("\ncalled getGroupMembers(). Return fault is {}".format(error.faultString))
        exit(1)
    except xmlrpcclient.ProtocolError as error:
        print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
            error.url, error.headers, error.errcode, error.errmsg))
        exit(1)

    for user in userList:
        try:
            notes = proxy.api.getUserProperty(auth, user, "notes")  # Get a list of groups for the current user of interest
            # print("Got group list {} for user {}".format(groups, user))
        except xmlrpcclient.Fault as error:
            print("\ncalled getUserProperty(). Return fault is {}".format(error.faultString))
            exit(1)
        except xmlrpcclient.ProtocolError as error:
            print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                error.url, error.headers, error.errcode, error.errmsg))
            exit(1)

        try:
            userInfo = loads(notes)
        except:
            userInfo = {}

        if not "expiry-date" in userInfo:
            userInfo['expiry-date'] =  (date.today() + timedelta(days=accountExpiry)).isoformat()
            print(userInfo['expiry-date'])
            try:
                proxy.api.setUserProperty(auth, user, "notes", dumps(userInfo))
            except xmlrpcclient.Fault as error:
                print("\ncalled setUserProperty(). Return fault is {}".format(error.faultString))
                exit(1)
            except xmlrpcclient.ProtocolError as error:
                print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                    error.url, error.headers, error.errcode, error.errmsg))
                exit(1)

        if date.fromisoformat(userInfo['expiry-date']) < date.today():
            try:
                proxy.api.deleteExistingUser(auth, user, True)
            except xmlrpc.client.Fault as error:
                print("\ncalled deleteExistingUser(). Return fault is {}".format(error.faultString))
                exit(1)
            except xmlrpc.client.ProtocolError as error:
                print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                  error.url, error.headers, error.errcode, error.errmsg))
                exit(1)

            print(f"Deleted user {user}")

    if len(userList) < limit:
        break # We have reached the end

    offset += limit # We need to next slice of users

