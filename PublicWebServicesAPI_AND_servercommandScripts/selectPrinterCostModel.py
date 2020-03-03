#!/usr/bin/env python3
# Find all the users in a specific user group

import xmlrpc.client
from ssl import create_default_context, Purpose
import sys

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then the client address will need to be whitelisted in PaperCut

auth="secret"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

#proxy = xmlrpc.client.ServerProxy(host, verbose=True, transport=xmlrpc.client.SafeTransport, context=ctx)
proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

serverName = "dipto-Latitude-7490"
printerName = "PDF"
propertyName = "cost-model"
propertyValue = "SIMPLE"


if len(sys.argv) != 4:
    print("Incomplete. Use: python3 selectPrinterCostModel.py [server_name] [printer_name] [property_value]")
    sys.exit(1)
else:
    serverName = sys.argv[1]
    printerName = sys.argv[2]
    propertyValue = sys.argv[3]
    print("server-command equivalent: server-command set-printer-property", serverName, propertyName, propertyValue)

#group = sys.argv[1]  # The user group of interest

try:
    command_feedback = proxy.api.setPrinterProperty(auth, serverName, printerName, propertyName, propertyValue)
    # print("Got user list {}".format(userList))
except xmlrpc.client.Fault as error:
    print("\ncalled setPrinterProperty. Return fault is {}".format(error.faultString))
    sys.exit(1)
except xmlrpc.client.ProtocolError as error:
    print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
        error.url, error.headers, error.errcode, error.errmsg))
    sys.exit(1)
except Exception as error:
    print("Error", error)
    sys.exit(1)


print("Feedback from the server :" , command_feedback)
