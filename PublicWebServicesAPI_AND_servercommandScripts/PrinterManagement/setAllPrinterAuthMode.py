#!/usr/bin/env python3


# NOTE: Needs PaperCut MF 19.1 or above


import xmlrpc.client
from ssl import create_default_context, Purpose
import sys

host = "https://localhost:9192/"

webServicesURL = host + "rpc/api/xmlrpc"


# Value defined in advanced config property "auth.webservices.auth-token". Should be random
auth = "token"

proxy  = xmlrpc.client.ServerProxy( webServicesURL, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))



settings = [
    ["advanced-config.ext-device.auth-mode.username-password", "Y"],
    ["advanced-config.ext-device.auth-mode.card", "Y"],
    ["advanced-config.ext-device.auth.pin-required-for-card", "N"],
    ["advanced-config.ext-device.self-association-with-card-enabled", "Y"],
    ["advanced-config.ext-device.self-association-allowed-card-regex", "^\d{4}$"], # Card numbers must be exactly 4 decimal digits
    ["advanced-config.ext-device.auth-mode.identity-no", "N"],
]

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

            splitID = sp.split("\\")

            if splitID[0]  != "device":
                continue  # It's a printer, don't bother

            deviceName = splitID[1]

            print(f"Configuring  device {deviceName}, result is {'success' if proxy.api.setPrinterProperties(auth, 'device', deviceName, settings) else 'failure'}")

        if len(printerList) < limit:
            break # We have reached the end

        offset += limit # We need to next slice of printers

