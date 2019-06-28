#!/usr/bin/env python3

"""
 List expired users that have expired or will expire soon, according to the expiry date written in their notes field in PaperCut.
 ...

 USAGE: listExpiredUsers.py [how_soon]
 It will list and identify users that have expired or will expire within the range of days specified.

 In PaperCut admin, please use the user's notes field to add an expiry date in the following format:
 expiry:yyyy-mm-dd
 e.g.
 expiry:2019-07-07
 ...
 
 PARAM: how_soon (integer)
 how_soon is the N number of days in the future.
 e.g. if today is 2019-07-07 and how_soon is 10, then it will look for records between today and 2019-07-17
 
 if parameter is not supplied it's defaulted to 0 and return users with expiry date in the past. 
  

""" 

import xmlrpc.client
from ssl import create_default_context, Purpose
import sys
import re
import datetime
from datetime import date, timedelta

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then the client address will need to be whitelisted in PaperCut

auth_token="testing"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

# listUsers method takes in optional n day range
def list_users(how_soon):
    offset = 0 
    limit = 100

    counter = 0
    unknown_list = []
     
    now = datetime.date.today()

    to_date = now + timedelta(days=how_soon)
    
    print("List of expiry dates until " +  to_date.strftime("%Y-%m-%d")+ ":")

    while True:
        try:
            #calls listUserAccount method of the API
            #return list of users
            user_list = proxy.api.listUserAccounts(auth_token, offset,limit)
        except xmlrpc.client.Fault as error:
            print("\ncalled listUserAccounts(). Return fault is {}".format(error.faultString))
            sys.exit(1)
        except xmlrpc.client.ProtocolError as error:
            print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                error.url, error.headers, error.errcode, error.errmsg))
            sys.exit(1)

        #return every user in the list
        for user in user_list:
            try:
                notes = proxy.api.getUserProperty(auth_token,user, "notes")
                match = re.search(r'expiry:\d{4}-\d{2}-\d{2}', notes.replace(" " , ""))
                if match is None :
                    unknown_list.append(user)
                    continue

                cleaned_match = match.group().strip("expiry:")
                date = datetime.datetime.strptime(cleaned_match, '%Y-%m-%d').date()
                status = ""

                if date < now:
                    status = "expired"
                    counter +=1
                    #HERE you could add user to delete list, or perform other action
                elif date == now :
                    status = "expires today"
                    counter +=1
                elif date <= to_date:
                    delta = date - now
                    status = "expiring in " + str(delta.days) + " day(s)"
                    
                # print output in pretty table
                if status != "":
                    print ("{:25s} {:13s} {:s}".format(user, str(date), status))

            except xmlrpc.client.Fault as error:
                print("\ncalled getUserProperty(). Return fault is {}".format(error.faultString))
                sys.exit(1)
            except xmlrpc.client.ProtocolError as error:
                print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                    error.url, error.headers, error.errcode, error.errmsg))
                sys.exit(1)
            except ValueError as error:
                print("Invalid date format or value in notes field. It must contain the word 'expiry:' followed by a date in yyyy-mm-dd format")

        if limit == 0 or len(user_list) < limit:
            break # We have reached the end

        offset += limit # We need to next slice of usersi

    #count how many users are expired until today including today
    plural =""
    are = "is"
    if counter>1:
        plural = "s"
        are = "are"
    print("\nThere " + are + " " + str(counter) +" expired user"+plural)

    print("\nUser(s) without any expiry date:")
    for user in unknown_list:
        print (user)


if __name__=="__main__":

    if len(sys.argv) == 1: #no argument, expired today and in the past
        list_users(0)
    elif len(sys.argv) == 2:
        try:
            offset_days = int(sys.argv[1])
            list_users(offset_days)
        except ValueError:
            print("Invalid number")
            sys.exit(1)
    else:
        print("Usage: ./listExpiredUsers.py [how_soon] or leave it blank to return all past record(s)")
       
