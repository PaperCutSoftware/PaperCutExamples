#!/usr/bin/env python3

# Small webb app to allow a user to top up thier personal PaperCut balance

# Add a custom URL to the PaperCut user web page, which is used by end users
# when they want to add credit to their PaperCut personal account. The url
# should refer to this small web app When the user clicks on the URL link
# (in the PaperCut user web page) to the web app, the user identification details
# are passed as part of the URL. This is explained at:

# https://www.papercut.com/products/ng/manual/common/topics/customize-user-web-pages.html#customize-user-web-pages-nav-links

# The URL neeeds to something like http://localhost:8081/simpleTopUpBalance/%user%?return_url=https%3A%2F%2Fgoogle.com

# This code is basic example only. It will require work before it can be used for production

import xmlrpc.client
import sys

# Bottle is a lightweight web framework
# pip install bottle
from bottle import route, run, template, request, debug, redirect


# Prefer HTTPS connection
# If not localhost then this address will need to be whitelisted in PaperCut
host = "http://localhost:9191/rpc/api/xmlrpc"
auth = "token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host)

redirect_url = ''


@route('/')
def wrongUrl():
    return("Please log into PaperCut and set top up your account from there")


@route('/simpleTopUpBalance/<user>')
def promptUser(user):
    # Redirect user to login page
    return_url = request.query.get("return_url")
    if return_url is None:
        return ("No return url provided, please return to PaperCut and try again")
    else:
        # Should probably verify URL is in correct format here
        global redirect_url
        redirect_url = return_url
    if not proxy.api.isUserExists(auth, user):
        return("Can't find user {}".format(user))

    return template('promptForDeposit', user=user)


@route('/topUp/<user>')
def topUp(user):
    if request.query.get('cancel', '').strip():
        return "Cancelled"

    amount = float(request.query.get('amount', '').strip())

    proxy.api.adjustUserAccountBalance(
        auth, user, amount, "Money added by the Simple Top Up Page")

    print('Updated balance is now {}. Returning user to {}'.format(
        proxy.api.getUserAccountBalance(auth, user), redirect_url))
    redirect(redirect_url)


run(host='localhost', port=8081, debug=True, reloader=True)
