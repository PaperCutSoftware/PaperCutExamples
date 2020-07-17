#!/usr/bin/env python3
"""
 List expired users that have expired or will expire soon, according to the expiry date written in their notes field in PaperCut.

 USAGE: listExpiredUsers.py [how_soon]
 It will list and identify users that have expired or will expire within the next "n" days

 In PaperCut admin, please use the user's notes field to add an expiry date in the following format:
 expiry:yyyy-mm-dd
 e.g.
 expiry:2019-07-07

 Users with no "expiry value in the notes field will assume to never expire.
 ...
 
 PARAM: how_soon (integer)

 Will list users who have already expired, or will expire in the next "how_soon" days
""" 

from  xmlrpc.client import ServerProxy, Fault, ProtocolError
from ssl import create_default_context, Purpose
from sys import exit, argv
from re import compile
from datetime import date, timedelta, datetime

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then the client address will need to be whitelisted in PaperCut

auth_token="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))


expireRE=compile(r'expiry:\d{4}-\d{2}-\d{2}')

# listUsers method takes in optional n day range
def list_users(how_soon):
    offset = 0 
    limit = 100

    counter = 0
    unknown_list = []

    today = date.today()

    check_date = today + timedelta(days=how_soon)
    
    print(f'List of expired users who have or will expire by {check_date.strftime("%Y-%m-%d")}:')

    while True:
        try:
            #calls listUserAccount method of the API
            #return list of users
            user_list = proxy.api.listUserAccounts(auth_token, offset,limit)
        except Fault as error:
            print("\ncalled listUserAccounts(). Return fault is {}".format(error.faultString))
            exit(1)
        except ProtocolError as error:
            print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                error.url, error.headers, error.errcode, error.errmsg))
            exit(1)

        #return every user in the list
        for user in user_list:
            try:
                notes = proxy.api.getUserProperty(auth_token,user, "notes")
            except xmlrpc.client.Fault as error:
                print("\ncalled getUserProperty(). Return fault is {}".format(error.faultString))
                exit(1)
            except xmlrpc.client.ProtocolError as error:
                print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                    error.url, error.headers, error.errcode, error.errmsg))
                exit(1)

            matchedNote = expireRE.search(notes)

            if matchedNote is None :
                # User has no expiry date -- no action required
                continue

            cleaned_match = matchedNote.group().strip("expiry:")

            expirtyDate = datetime.strptime(cleaned_match, '%Y-%m-%d').date()

            status = ""

            if expirtyDate < check_date:
                status = "expired"
                counter += 1
                if expirtyDate > today:
                    print (f"{user} will expire on {expirtyDate}")
                else:
                    print (f"{user} has expired {expirtyDate}")
                
                #HERE you could add user to delete list, or perform other action

        if limit == 0 or len(user_list) < limit:
            break # We have reached the end

        offset += limit # We need to next slice of users

    if counter == 0:
        print(f"\nThere are no expiring users")
    elif counter>1:
        print(f"\nThere are {counter} expiring users")
    else:
        print(f"\nThere is one expiring user")

if __name__=="__main__":

    if len(argv) == 1: #no argument, expired today and in the past
        list_users(0)
    elif len(argv) == 2:
        try:
            offset_days = int(argv[1])
            list_users(offset_days)
        except ValueError:
            print("Usage: ./listExpiredUsers.py [how_soon] or leave it blank to return all past record(s)")
    else:
        print("Usage: ./listExpiredUsers.py [how_soon] or leave it blank to return all past record(s)")
