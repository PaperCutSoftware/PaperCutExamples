#!/usr/bin/env python3

# Load a lot of data and use getTaskStatus()

import xmlrpc.client
from time import sleep
from sys import exit

host="http://localhost:9191/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth="password"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random
# Generate a file of data


print("Creating Data Import file")

fileName = "/tmp/import.file"

f = open(fileName, 'w')

for p in range(20):
    f.write("parentAccount{}\t\t\t\t\t\t\t\t\t\t\n".format(p))
    for a in range(100):
        f.write("{}LongParentAccountname\t{}ReallyLongSharedAccountName\t\t{}x{}\t10\t\t\t[All Users]\t\t\t\n".format(p, a, p, a))

f.close()
print("Data Import file created")

proxy = xmlrpc.client.ServerProxy(host)

print("Starting Data File Upload")

try:
    proxy.api.batchImportSharedAccounts(auth, fileName, False, False)
except xmlrpc.client.Fault as error:
    print("\ncalled batchImportSharedAccounts(). Return fault is {}".format(error.faultString))
    sys.exit(1)
except xmlrpc.client.ProtocolError as error:
    print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
        error.url, error.headers, error.errcode, error.errmsg))
    sys.exit(1)

status = proxy.api.getTaskStatus()
while not status["completed"]:
    sleep(3) # Wait three seconds so server is not overloaded
    print(".",end="", flush=True)  # Show the user something is happing
    status = proxy.api.getTaskStatus()

# Only want the last line of messages
last=status["message"].splitlines()[-1]

print("\n{}".format(last))

