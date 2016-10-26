#!/usr/bin/env python3

# If a user has staretd using a temp card this job will remove the card from the card field

import xmlrpc.client
import sys

host="http://localhost:9191/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth="password"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host)

cardDatabase = [  #  List of the tempcards
    "1234",
    "2345",
    "3456",
]

for card in cardDatabase:
    username = proxy.api.lookUpUserNameByCardNo(auth, card)
    print("Looking up card {}".format(card))
    if len(username) > 0:
        if proxy.api.getUserProperty(auth, username, "primary-card-number") == card:
            print("Removing card number {} from primary card field for user {}".format(card, username))
            proxy.api.setUserProperty(auth, username, "primary-card-number", "")
        elif proxy.api.getUserProperty(auth, username, "secondary-card-number") == card:
            print("Removing card number {} from secondary card field for user {}".format(card, username))
            proxy.api.setUserProperty(auth, username, "secondary-card-number", "")
        else:
            print("Error can't find card number")

