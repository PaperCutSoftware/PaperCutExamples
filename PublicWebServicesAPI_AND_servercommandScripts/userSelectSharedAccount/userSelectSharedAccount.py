#!/usr/bin/env python3

# Small webb app to allow a user to change their shared account

# Add a custom URL to the PaperCut user web page, which is used by end users
# when they want to change their default PaperCut shared account. The url
# should refer to this small web app When the user clicks on the URL link
# (in the PaperCut user web page) to the web app, the user identification details
# is passed as part of the URL. This is explained at:

# https://www.papercut.com/support/resources/manuals/ng-mf/common/topics/customize-user-web-pages.html#customize-user-web-pages-nav-links

# The URL neeeds to something like http://localhost:8080/getsharedaccountselection/%user%

# This code is basic example only. It will require work before it can be used for production

import xmlrpc.client
import sys

# Bottle does not depend on any external libraries.
# You can just download bottle.py into your project directory and using
# $ wget http://bottlepy.org/bottle.py
from bottle import route, run, template, request, debug

host="http://localhost:9191/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut
auth="password"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host)

@route('/')
def wrongUrl():
    return("Please log into PaperCut and set your shared account from there")

@route('/getsharedaccountselection/<user>')
def setSharedAccount(user):

    if not proxy.api.isUserExists(auth, user):
        return("Can't find user {}".format(user))

    shared_accounts = proxy.api.listUserSharedAccounts(auth, user, 0, 99, True)

    if len(shared_accounts) == 0:
        return "User {} has no access to shared accounts".format(user)

    return template('displayAccounts',user=user,rows=shared_accounts)


@route('/setdefaultsharedaccount/<user>')
def changeAccountTo(user):
    if request.GET.get('cancel','').strip():
        return "Cancelled"

    selectedAccount = request.GET.get('account','').strip()

    proxy.api.setUserAccountSelectionAutoSelectSharedAccount(auth,user,selectedAccount, False)

    return 'Changed default account to "{}"<br><br>Please close this tab/window and return to PaperCut'.format(selectedAccount)

run(host='localhost', port=8080, debug=True, reloader=True)

