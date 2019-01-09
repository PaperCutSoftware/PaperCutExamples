#!/usr/bin/env python3

from  csv import reader
from sys import stdin

from xmlrpc.client import ServerProxy
from ssl import create_default_context, Purpose


# #TODO Add a note about which report this example works with.


host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth="token"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random

proxy = ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

csv_reader = reader(stdin,  delimiter=',')
line_count = 0
for row in csv_reader:
    if line_count == 2:
        row.insert(4,"Notes data")
    elif line_count > 2:
        row.insert(4,proxy.api.getSharedAccountProperty(auth, row[0] + "\\" + row[2], "notes"))
    print(", ".join(row))
    line_count += 1
