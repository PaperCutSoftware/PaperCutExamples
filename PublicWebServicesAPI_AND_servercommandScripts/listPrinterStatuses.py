#!/usr/bin/env python3

import xmlrpc.client
from ssl import create_default_context, Purpose
import sys
import requests

# To use tls see http://docs.python-requests.org/en/master/user/advanced/
host = "http://localhost:9191/"


healthURL = host + "api/health/{}/{}/status"
webServicesURL = host + "rpc/api/xmlrpc"

# See https://www.papercut.com/support/resources/manuals/ng-mf/common/topics/tools-monitor-system-health-api-authorization-key.html
healthAuth = {'Authorization':"XrACcfMNEtfxnEpXeawi52mRneEwkXYd"}

# Value defined in advanced config property "auth.webservices.auth-token". Should be random
auth = "token"

proxy  = xmlrpc.client.ServerProxy( webServicesURL, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

def getDevicePrinterID(server, printer):

    try:
        return proxy.api.getPrinterProperty(auth, server, printer, "printer-id" )
    except xmlrpc.client.Fault as error:
        # If the printer is not found this exception will get thrown
        print("\ncalled getPrinterProperty(). Return fault is {}".format(error.faultString))
        sys.exit(1)
    except xmlrpc.client.ProtocolError as error:
        print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
            error.url, error.headers, error.errcode, error.errmsg))
        sys.exit(1)
    
def getDevicePrinterStatus(server, printer):

    printerID = getDevicePrinterID(server, printer)

    if server == "device":
        type="devices"
    else:
        type="printers"

    try:
        printerStatusResponse = requests.get( healthURL.format(type, printerID), headers=healthAuth)
    except ConnectionError as error:
        print("Network problem calling health API: {}".format(error))
        sys.exit(1)
    except requests.exceptions.Timeout as error:
        print("Network call to  health API timed out: {}".format(error))
        sys.exit(1)
    except requests.exceptions.RequestException as error:
        print("Network error on health API failed: {}".format(error))
        sys.exit(1)

    try:
        jsonResponse = printerStatusResponse.json()
    except ValueError as error:
        print("Could decode json from health API: {}".format(error))
        sys.exit(1)

    return printerStatusResponse.status_code, jsonResponse["status"]


if __name__ == "__main__":
    # execute only if run as a script

    offset = 0

    limit = 100 # Max number of printers to retrieve on each call

    while True:
        try:
            printerList = proxy.api.listPrinters(auth, offset,limit)
        except xmlrpc.client.Fault as error:
            print("\ncalled listPrinters(). Return fault is {}".format(error.faultString))
            sys.exit(1)
        except xmlrpc.client.ProtocolError as error:
            print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                error.url, error.headers, error.errcode, error.errmsg))
            sys.exit(1)

        for sp in printerList:
            if sp == "!!template printer!!":
                continue
            splitID = sp.split("\\")
            server= splitID[0]
            printer = splitID[1]

            status, text = getDevicePrinterStatus(server, printer)

            if server == "device":
                type="device"
            else:
                type="printer"

            if status != 200:
                print("Status for {} {}/{} is {} -- DEVICE/PRINTER IN ERROR".format(
                    type,
                    server,
                    printer,
                    text))
            else:
                print("Status for {} {}/{} is {}".format(
                    type,
                    server,
                    printer,
                    text))

        if len(printerList) < limit:
            break # We have reached the end

        offset += limit # We need to next slice of printers

