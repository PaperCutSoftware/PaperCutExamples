#!/usr/bin/env python

# Must be Python 3.6 or above

helpText="""

This script will configure a virtual find me Q for release and printing on multiple devices using find me printing.

It designed to support MFD based release stations, as explained at

https://www.papercut.com/support/resources/manuals/ng-mf/applicationserver/topics/device-mf-copier-integration-release-multiple-operating-systems.html

Note: Needs PaperCut MF 2.0.3 or above

For simplicity this script configures a single hold release queue with multiple MFD queues. It can be extended for more
complex requirements

A print queue must already be created that can be configured as a virtual queue. The physical print queues for each MFD must also be defined in PaperCut MF. 

Usage: ./find-me-automation.py [server of virtual q]\[virtual q name]  [csv input files containing printer info]...

CSV files must be in the following format and must NOT contain a header line

<mfd-device-name>,<print-server-name>\<print queue name>,...
...

each line contains the A) the MFD that will run the release station and B) a list of physical printer server and queue names

Note that each MFD release station can support multiple print server operating systems as described in the above documentation.
"""

import xmlrpc.client
from ssl import create_default_context, Purpose
from sys import argv, exit
from csv import DictReader

host = "https://localhost:9192/rpc/api/xmlrpc"

# Value defined in advanced config property "auth.webservices.auth-token". Should be random
auth = "password"

proxy  = xmlrpc.client.ServerProxy( host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

server_command=proxy.api

print( "----------------------------")
print( "Find Me Queue Automation")
print( "----------------------------")

if len(argv) < 3 :
  exit( f"Incorrect input params Exiting...{helpText}")
  
split = argv[1].split("\\",1)
if not len(split) == 2:
  exit(f"Invalid virtual queue name supplied {argv[1]}")


virtual_Q_server = split[0].strip()
virtual_Q_printer = split[1].strip()

print( f"Configuring Printer: {virtual_Q_server}/{virtual_Q_printer} for find me release")

queue_list = list()
printIDlist = list()

for file in argv[2:]:  # Loop over each file on the command line

  with open(file, newline='') as csvfile:

    printQConfigReader = DictReader(csvfile,  fieldnames=["MFD"], restkey="printQueues")
    for prt in printQConfigReader:

      print(f"{prt}")
      mfd_id = server_command.getPrinterProperty(auth, "device", prt['MFD'], "printer-id")

      print(f"MFD id for {prt['MFD']} is {mfd_id}")

      printQlist = list()
      for p in prt['printQueues']:
        split = p.split("\\",1)
        if not len(split) == 2:
            exit(f"Invalid data supplied {prt}")

        server_name = split[0].strip()
        printer_name = split[1].strip()

        print( f"Adding physical printer {server_name}/{printer_name}")
        printer_id = server_command.getPrinterProperty(auth, server_name, printer_name, "printer-id")

        printIDlist.append(printer_id) # Save this list of all printer ids for virtual q config

        printQlist.append({'server-name':server_name, 'printer-name':printer_name, 'printer-id':printer_id})
      
      record = {"q-list": printQlist, "mfd-name": prt['MFD'], "mfd-id": mfd_id}
      queue_list.append(record)

print(queue_list)

print( f"Setting Printer: {virtual_Q_printer} to hold print jobs\nApplying redirect queues {printIDlist} to {virtual_Q_printer}")

server_command.setPrinterProperties(auth, virtual_Q_server, virtual_Q_printer,
            [["virtual", "True"],
             ["advanced-config.release-station", "STANDARD"],
             ["advanced-config.redirect.compatible-queues", ",".join(printIDlist)]])

virtual_id = server_command.getPrinterProperty(auth, virtual_Q_server, virtual_Q_printer, "printer-id")

for prt in queue_list:

  print( f"Checking Device: {prt['mfd-name']} is a Release Station")

  device_functions = server_command.getPrinterProperty(auth,"device", prt['mfd-name'], "device-functions")

  if not "RELEASE_STATION" in device_functions:
    print(f"Adding RELEASE_STATION to {prt['mfd-name']} functions")
    server_command.setPrinterProperty(auth, "device", prt['mfd-name'], "device-functions", device_functions + ",RELEASE_STATION")

  print( f"Setting redirect queues")

  qListID = ','.join([x['printer-id'] for x in prt['q-list']])

  server_command.setPrinterProperties(auth, "device", prt['mfd-name'],
            [["advanced-config.ext-device.assoc-printers", virtual_id ],
             ["advanced-config.ext-device.releases-on", qListID]])

  if len(prt["q-list"]) > 1:  #TODO
    print(f"setting {prt['mfd-name']} to MULTIPLE_QUEUES")
    server_command.setPrinterProperty(auth, "device", prt['mfd-name'], "advanced-config.ext-device.find-me-release-mode", "MULTIPLE_QUEUES")

  print( "Restarting device")
  server_command.applyDeviceSettings(auth, prt['mfd-name'])

#Done
