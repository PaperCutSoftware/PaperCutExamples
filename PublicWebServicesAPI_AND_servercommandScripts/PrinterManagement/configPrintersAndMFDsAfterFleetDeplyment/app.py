#!/usr/bin/env python

import csv
import xmlrpc.client
from ssl import create_default_context, Purpose
from sys import argv, exit
import re
import pprint

pprint = pprint.pformat


serverPrinterSplitter = re.compile(r'\\')

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut
auth="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

# with open('batch-devices-FX-New.csv', newline='') as csvfile:

for file in argv[1:]:
    with open(file, newline='') as csvfile:
        deviceConfigReader = csv.DictReader(csvfile)
        for row in deviceConfigReader:

            if "deviceType" in row:
                # it's an MFD

                print("Found an MFD")
                
                server, printer = "device", row['deviceName']

                configData = (            
                        ("cost-model","SIZE_TABLE")
                        ,("advanced-config.cost.pst.default.enabled", "Y")
                        ,("advanced-config.cost.pst.default.color.duplex", f"{row['copy-cost:default.color.duplex']}")
                        ,("advanced-config.cost.pst.default.color.simplex", f"{row['copy-cost:default.color.simplex']}")
                        ,("advanced-config.cost.pst.default.grayscale.duplex", f"{row['copy-cost:default.grayscale.duplex']}")
                        ,("advanced-config.cost.pst.default.grayscale.simplex", f"{row['copy-cost:default.grayscale.simplex']}")
                        ,("advanced-config.cost.pst.A4.enabled", "Y")
                        ,("advanced-config.cost.pst.A4.color.duplex", f"{row['copy-cost:default.color.duplex']}")
                        ,("advanced-config.cost.pst.A4.color.simplex", f"{row['copy-cost:default.color.simplex']}")
                        ,("advanced-config.cost.pst.A4.grayscale.duplex", f"{row['copy-cost:default.grayscale.duplex']}")
                        ,("advanced-config.cost.pst.A4.grayscale.simplex", f"{row['copy-cost:default.grayscale.simplex']}")
                        ,("advanced-config.cost.pst.A3.enabled", "Y")
                        ,("advanced-config.cost.pst.A3.color.duplex", f"{row['copy-cost:A3.color.duplex']}")
                        ,("advanced-config.cost.pst.A3.color.simplex", f"{row['copy-cost:A3.color.simplex']}")
                        ,("advanced-config.cost.pst.A3.grayscale.duplex", f"{row['copy-cost:A3.grayscale.duplex']}")
                        ,("advanced-config.cost.pst.A3.grayscale.simplex", f"{row['copy-cost:A3.grayscale.simplex']}")
                        ,("advanced-config.ext-device.auth-mode.username-password", f"{row['auth-mode.username-password']}")
                        ,("advanced-config.ext-device.auth-mode.card", f"{row['ext-device.auth-mode.card']}")
                        ,("advanced-config.ext-device.self-association-with-card-enabled", f"{row['self-association-with-card-enabled']}")
                        )

            else:
                # it's a printer
                print("Found a printer")

                server, printer = serverPrinterSplitter.split(row["printQueue"], maxsplit=2)

                configData = (
                    ("cost-model","SIZE_TABLE")  # Note hard coded
                    ,("advanced-config.cost.pst.default.enabled", "Y")
                    ,("advanced-config.cost.pst.default.color.duplex", f"{row['page-cost:default.color.duplex']}")
                    ,("advanced-config.cost.pst.default.color.simplex", f"{row['page-cost:default.color.simplex']}")
                    ,("advanced-config.cost.pst.default.grayscale.duplex", f"{row['page-cost:default.grayscale.duplex']}")
                    ,("advanced-config.cost.pst.default.grayscale.simplex", f"{row['page-cost:default.grayscale.simplex']}")
                    ,("advanced-config.cost.pst.A4.enabled", "Y")
                    ,("advanced-config.cost.pst.A4.color.duplex", f"{row['page-cost:default.color.duplex']}")
                    ,("advanced-config.cost.pst.A4.color.simplex", f"{row['page-cost:default.color.simplex']}")
                    ,("advanced-config.cost.pst.A4.grayscale.duplex", f"{row['page-cost:default.grayscale.duplex']}")
                    ,("advanced-config.cost.pst.A4.grayscale.simplex", f"{row['page-cost:default.grayscale.simplex']}")
                    ,("advanced-config.cost.pst.A3.enabled", "Y")
                    ,("advanced-config.cost.pst.A3.color.duplex", f"{row['page-cost:A3.color.duplex']}")
                    ,("advanced-config.cost.pst.A3.color.simplex", f"{row['page-cost:A3.color.simplex']}")
                    ,("advanced-config.cost.pst.A3.grayscale.duplex", f"{row['page-cost:A3.grayscale.duplex']}")
                    ,("advanced-config.cost.pst.A3.grayscale.simplex", f"{row['page-cost:A3.grayscale.simplex']}")
                    ,("advanced-config.watermark.enabled", f"{row['watermark.enabled']}")
                    ,("advanced-config.watermark.text", f"{row['watermark.text']}")
                    ,("advanced-config.watermark.font-size", f"{row['watermark.font-size']}")
                    ,("advanced-config.watermark.gray-level", f"{row['watermark.gray-level']}")
                    ,("advanced-config.watermark.position", f"{row['watermark.position']}")
                )

#            print(f"server = {server}, device = {printer}, config data = {pprint(configData)}")
            try:
                # Setup device/printer
                resp = proxy.api.setPrinterProperties(auth, server, printer, configData)
                if server == "device":  # MFD needs a restart to get updates
                    resp = proxy.api.applyDeviceSettings(auth, printer)


            except xmlrpc.client.Fault as error:
                print(f"\ncalled setPrinterProperties(). Return fault is {error.faultString}")
                exit(1)
            except xmlrpc.client.ProtocolError as error:
                print(f"\nA protocol error occurred\nURL: {error.url}\nHTTP/HTTPS headers: {error.headers}\n"
                    f"Error code: {error.errcode}\nError message: {error.errmsg}")
                exit(1)
            except ConnectionRefusedError as error:
                print("Connection refused. Is the Papercut server running?")
                exit(1)
