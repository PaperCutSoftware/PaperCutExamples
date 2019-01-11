#!/usr/bin/env python3

# Small webb app to allow a user to  request a refund of their personal PaperCut balance
# into another system

# Add a custom URL to the PaperCut user web page, which is used by end users
# when they want to request a refund from their PaperCut personal account. The url
# should refer to this small web app When the user clicks on the URL link
# (in the PaperCut user web page) to the web app, the user identification details
# are passed as part of the URL. This is explained at:

# https://www.papercut.com/products/ng/manual/common/topics/customize-user-web-pages.html#customize-user-web-pages-nav-links

# The URL neeeds to something like http://localhost:8081/simpleRefundBalance/%user%

# This code is basic example only. It will require work before it can be used for production

import xmlrpc.client
import sys
from ssl import create_default_context, Purpose

# Bottle does not depend on any external libraries.
# You can just download bottle.py into your project directory and using
# $ wget http://bottlepy.org/bottle.py
from bottle import route, run, template, request, debug


# Prefer HTTPS connection
host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut
auth="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

@route('/')
def wrongUrl():
    return("Please log into PaperCut and chose refund your account balance from there")

@route('/simpleRefundBalance/<user>')
def promptUser(user):

    if not proxy.api.isUserExists(auth, user):
        return("Can't find user {}".format(user))

    userCredit = "{0:.2f}".format(proxy.api.getUserAccountBalance(auth, user))

    return template('promptForRefund',user=user, userCredit=userCredit)

@route('/refund/<user>')
def topUp(user):
    if request.GET.get('cancel','').strip():
        return "Refund cancelled by {}".format(user)

    refundAmount = float(request.GET.get('amount','').strip())

    userCredit = proxy.api.getUserAccountBalance(auth, user)

    if userCredit != refundAmount:
        return "Error: User Credit Balance and Refund Requested do not match for user: {}".format(user)

    proxy.api.adjustUserAccountBalance(auth, user, -1 * refundAmount, "Money refunded by the Simple Refund Page")

    return 'Updated balance is now {}<br><br>Please close this tab/window and return to PaperCut'.format(
            "{0:.2f}".format(proxy.api.getUserAccountBalance(auth, user)))

    # now transfer the value to the external student system

run(host='localhost', port=8081, debug=True, reloader=True)

