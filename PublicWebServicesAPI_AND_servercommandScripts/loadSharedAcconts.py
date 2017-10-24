#!/usr/bin/env python3

# Load a lot of data and use getTaskStatus()

import xmlrpc.client

host="http://localhost:9191/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth="password"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random
# Generate a file of data

fileName = "/tmp/import.file"

f = open(fileName, 'w')

for p in range(20):
    f.write("parentAccount{}\t\t\t\t\t\t\t\t\t\t\n".format(p))
    for a in range(100):
        f.write("{}LongParentAccountname\t{}ReallyLongSharedAccountName\t\t{}x{}\t10\t\t\t[All Users]\t\t\t\n".format(p, a, p, a))

f.close()

proxy = xmlrpc.client.ServerProxy(host)

proxy.api.batchImportSharedAccounts(auth, fileName, False, False)

status = proxy.api.getTaskStatus()
while not status["completed"]:
    status = proxy.api.getTaskStatus()

print("{}\n".format(status["message"]))

