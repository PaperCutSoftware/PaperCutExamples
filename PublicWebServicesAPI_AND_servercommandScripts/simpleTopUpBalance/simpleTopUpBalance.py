#!/usr/bin/env python

# Small web app to allow a user to top up their personal PaperCut balance

# Add a custom URL to the PaperCut user web page, which is used by end users
# when they want to add credit to their PaperCut personal account. The url
# should refer to this small web app When the user clicks on the URL link
# (in the PaperCut user web page) to the web app, the user identification details
# are passed as part of the URL. This is explained at:

# https://www.papercut.com/products/ng/manual/common/topics/customize-user-web-pages.html#customize-user-web-pages-nav-links

# The URL neeeds to something like http://localhost:8081/simpleTopUpBalance/?user=%user%&return_url=%return_url%

# Generally additional security should be provided. For example if the URL is http://localhost:8081/promptForPassword/?user=%user%&return_url=%return_url%
# then the user will need to enter their PaperCut password to access the payment system

# Handy Tip: By default the link will open in a separate winodow. You can edit the advanced config property user.web.custom-links and
# change "_body" to "_self". You should then use the %return_url% to return the user to the PaperCut MF/NG web interface

# This code is a basic example only. It should not be used for production

import xmlrpc.client
import sys
from json import load as loadjs
import logging
import traceback

# Bottle does not depend on any external libraries.
# You can just download bottle.py into your project directory and using
# $ wget http://bottlepy.org/bottle.py
from bottle import route, run, template, request, debug, response


# Prefer HTTPS connection
# If not localhost then this address will need to be whitelisted in PaperCut
host = "http://localhost:9191/rpc/api/xmlrpc"
auth = "token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host)

# For more information on this user database file refer to the custom auth and sync demo
paperCutAccountInfoFile = 'c:\\Program Files\\PaperCut MF\\server\\custom\\config.json'

paperCutAccountData = {}

# The user is sent back to the Summary page as if they had just logged in,
# assuming their session has not timed out
# Therefore return url should be consistent
redirect_url = ''


@route('/')
def wrongUrl():
    return("Please log into PaperCut and set top up your account from there")


@route('/promptForPassword/')
def prompForPassword():

    user = request.query.user or ""

    try:
        if len(user) == 0 or not proxy.api.isUserExists(auth, user):
            return( "Can't find user {}".format(user))
    except Exception as e:
        logging.error(traceback.format_exc())
    
    return_url = request.query.return_url or ""

    return template( 'promptForPassword', user=user, return_url=return_url)

@route('/simpleTopUpBalance/', method='GET')
def promptUser():

    user = request.query.user or ""

    return_url = request.query.return_url or ""

    password = request.query.password or ""

    if paperCutAccountData is None or paperCutAccountData['userdata'][user]['password'] == password:
        return template('promptForDeposit',user=user, return_url=return_url)

    # Password validation failed    
    return template( 'promptForPassword', user=user, error_text="Invalid password entered", return_url=return_url)


@route("/topUp/")
def topUp(method="GET"):

    return_url = request.query.return_url or None

    if request.query.cancel == "cancel":
        if return_url is None:
            return "Cancelled. Please close this tab/window and return to PaperCut"
        else:
            response.set_header("Refresh", "5; url={}".format(return_url))
            return "Cancelled. You will be returned to PaperCut in 5s"

    user = request.query.user

    amount = float(request.query.amount)

    if not amount > 0.0: # Example of data validation -- not used because our form already does this one
        return template('promptForDeposit',user=user, return_url=return_url, error_text="Invalid amount \"{}\" entered".format(amount))

    proxy.api.adjustUserAccountBalance(
        auth, user, amount, "Money added by the Simple Top Up Page")

    if len(return_url) == 0:
        return "Updated balance is now {}<br><br>Please close this tab/window and return to PaperCut".format(
            proxy.api.getUserAccountBalance(auth,user))

    # Add refresh with 5s timeout back to PaperCut MF/NG
    response.set_header("Refresh", "5; url={}".format(return_url))
    return "Updated balance is now {}<br><br>You will be returned to PaperCcut in 5s".format(
            proxy.api.getUserAccountBalance(auth,user))

try:
    with open(paperCutAccountInfoFile) as f:
        paperCutAccountData = loadjs(f)
except OSError:
    paperCutAccountData = None

run(host='localhost', port=8081, debug=True, reloader=True)
