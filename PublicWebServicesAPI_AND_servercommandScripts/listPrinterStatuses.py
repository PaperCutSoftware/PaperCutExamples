#!/usr/bin/env python3

import xmlrpc.client
from ssl import create_default_context, Purpose
import sys
import requests

host = "http://localhost:9191/"

healthURL = host + "api/health/printers/{}/status"
webServicesURL = host + "rpc/api/xmlrpc"

healthAuth = {'Authorization':"XrACcfMNEtfxnEpXeawi52mRneEwkXYd"}
auth = "token"

proxy  = xmlrpc.client.ServerProxy( webServicesURL, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))


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
        if server == "device":
          continue
        try:
            printerID = proxy.api.getPrinterProperty(auth, server, printer, "printer-id" )
        except xmlrpc.client.Fault as error:
            print("\ncalled getPrinterProperty(). Return fault is {}".format(error.faultString))
            sys.exit(1)
        except xmlrpc.client.ProtocolError as error:
            print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
                error.url, error.headers, error.errcode, error.errmsg))
            sys.exit(1)
        
        try:
          printerStatusResponse = requests.get( healthURL.format(printerID), headers=healthAuth)
        except ConnectionError as error:
          print("Network problem calling health API: {}".format(error))
          sys.exit(1)
        except Timeout as error:
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


        if printerStatusResponse.status_code != 200:
            print("Status for printer {}/{} is {}  -- PRINTER IN ERROR ".format(
                  server,
                  printer,
                  jsonResponse["status"]))
        else:
            print("Status for printer {}/{} is {}".format(
                  server,
                  printer,
                  jsonResponse["status"]))

    if len(printerList) < limit:
        break # We have reached the end

    offset += limit # We need to next slice of printers

