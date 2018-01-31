#!/usr/bin/env python3

# Small webb app to allow a user to top up thier personal PaperCut balance

# Add a custom URL to the PaperCut user web page, which is used by end users
# when they want to add credit to their PaperCut personal account. The url
# should refer to this small web app When the user clicks on the URL link
# (in the PaperCut user web page) to the web app, the user identification details
# is passed as part of the URL. This is explained at:

# https://www.papercut.com/products/ng/manual/common/topics/customize-user-web-pages.html#customize-user-web-pages-nav-links

# The URL neeeds to something like http://localhost:8081/simpleTopUpBalance/%user%

# This code is basic example only. It will require work before it can be used for production

import xmlrpc.client
import sys

# Bottle does not depend on any external libraries.
# You can just download bottle.py into your project directory and using
# $ wget http://bottlepy.org/bottle.py
from bottle import route, run, template, request, debug

host="http://localhost:9191/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut
auth="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host)

@route('/')
def wrongUrl():
    return("Please log into PaperCut and set top up your account from there")

@route('/simpleTopUpBalance/<user>')
def setSharedAccount(user):

    if not proxy.api.isUserExists(auth, user):
        return("Can't find user {}".format(user))

    return template('promptForDeposit',user=user)

@route('/topUp/<user>')
def topUp(user):
    if request.GET.get('cancel','').strip():
        return "Cancelled"

    amount = float(request.GET.get('amount','').strip())

    proxy.api.adjustUserAccountBalance(auth, user, amount, "Money added by the Simple Top Up Page");

    return 'Updated balance is now {}<br><br>Please close this tab/window and return to PaperCut'.format(
            proxy.api.getUserAccountBalance(auth,user))

run(host='localhost', port=8081, debug=True, reloader=True)

