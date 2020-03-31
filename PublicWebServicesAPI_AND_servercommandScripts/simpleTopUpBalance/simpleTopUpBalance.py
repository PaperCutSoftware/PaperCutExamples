#!/usr/bin/env python3

# Small webb app to allow a user to top up thier personal PaperCut balance

# Add a custom URL to the PaperCut user web page, which is used by end users
# when they want to add credit to their PaperCut personal account. The url
# should refer to this small web app When the user clicks on the URL link
# (in the PaperCut user web page) to the web app, the user identification details
# are passed as part of the URL. This is explained at:

# https://www.papercut.com/products/ng/manual/common/topics/customize-user-web-pages.html#customize-user-web-pages-nav-links

<<<<<<< HEAD
# The URL neeeds to something like http://localhost:8081/simpleTopUpBalance/?user=%user%&return_url=%return_url%
=======
# The URL neeeds to something like http://localhost:8081/simpleTopUpBalance/%user%?return_url=https%3A%2F%2Fgoogle.com
>>>>>>> e6ed9af1fed4f3615da2bf3aa14d9993abf532d4

# This code is basic example only. It will require work before it can be used for production

import xmlrpc.client
import sys

<<<<<<< HEAD
# Bottle does not depend on any external libraries.
# You can just download bottle.py into your project directory and using
# $ wget http://bottlepy.org/bottle.py
from bottle import route, run, template, request, debug, response
=======
# Bottle is a lightweight web framework
# pip install bottle
from bottle import route, run, template, request, debug, redirect
>>>>>>> e6ed9af1fed4f3615da2bf3aa14d9993abf532d4


# Prefer HTTPS connection
# If not localhost then this address will need to be whitelisted in PaperCut
host = "http://localhost:9191/rpc/api/xmlrpc"
auth = "token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host)

# The user is sent back to the Summary page as if they had just logged in,
# assuming their session has not timed out
# Therefore return url should be consistent
redirect_url = ''


@route('/')
def wrongUrl():
    return("Please log into PaperCut and set top up your account from there")

<<<<<<< HEAD
@route('/simpleTopUpBalance/')
def promptUser():

    user = request.query.user or ""

    return_url = request.query.return_url or ""
    
    if len(user) == 0 or not proxy.api.isUserExists(auth, user):
        return("Can't find user {}".format(user))

    return template('promptForDeposit',user=user, return_url=return_url)

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
=======

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
>>>>>>> e6ed9af1fed4f3615da2bf3aa14d9993abf532d4

    proxy.api.adjustUserAccountBalance(
        auth, user, amount, "Money added by the Simple Top Up Page")

<<<<<<< HEAD
    if len(return_url) == 0:
        return "Updated balance is now {}<br><br>Please close this tab/window and return to PaperCut".format(
            proxy.api.getUserAccountBalance(auth,user))

    # Add refresh with 5s timeout back to PaperCut MF/NG
    response.set_header("Refresh", "5; url={}".format(return_url))
    return "Updated balance is now {}<br><br>You will be returned to PaperCcut in 5s".format(
            proxy.api.getUserAccountBalance(auth,user))
=======
    print('Updated balance is now {}. Returning user to {}'.format(
        proxy.api.getUserAccountBalance(auth, user), redirect_url))
    redirect(redirect_url)

>>>>>>> e6ed9af1fed4f3615da2bf3aa14d9993abf532d4

run(host='localhost', port=8081, debug=True, reloader=True)
