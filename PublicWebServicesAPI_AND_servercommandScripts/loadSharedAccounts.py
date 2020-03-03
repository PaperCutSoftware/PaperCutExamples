#!/usr/bin/env python3

# Load a lot of data and use getTaskStatus()

import xmlrpc.client
from ssl import create_default_context, Purpose
from time import sleep
from sys import exit

host="https://localhost:9192/rpc/api/xmlrpc" # If not localhost then this address will need to be whitelisted in PaperCut

auth="password"  # Value defined in advanced config property "auth.webservices.auth-token". Should be random
# Generate a file of data


print("Creating Data Import file")

fileName = "/tmp/import.file"

f = open(fileName, 'w')

for p in range(20):
    f.write("parentAccount{0:02}\t\tY\tPPx{0:02}\t10.0\tN\t[All Users]\t\t\t\t\n".format(p))
    for a in range(100):
        f.write("{0:02}LongParentAccountname\t{1:02}ReallyLongSharedAccountName\t\t{0:02}x{1:02}\t10.0\t\t\t[All Users]\t\t\t\n".format(p, a))

f.close()
print("Data Import file created")

proxy = xmlrpc.client.ServerProxy(host, verbose=False,
      context = create_default_context(Purpose.CLIENT_AUTH))

print("Starting Data File Upload")

try:
    proxy.api.batchImportSharedAccounts(auth, fileName, False, False)
except xmlrpc.client.Fault as error:
    print("\ncalled batchImportSharedAccounts(). Return fault is {}".format(error.faultString))
    exit(1)
except xmlrpc.client.ProtocolError as error:
    print("\nA protocol error occurred\nURL: {}\nHTTP/HTTPS headers: {}\nError code: {}\nError message: {}".format(
        error.url, error.headers, error.errcode, error.errmsg))
    exit(1)

status = proxy.api.getTaskStatus()
lineCount = 0
while not status["completed"]:
    sleep(3) # Wait three seconds so server is not overloaded
    print(".",end="", flush=True)  # Show the user something is happing
    print("\nStatus: {}\t Message: {}".format(status['completed'],status['message'].splitlines()[lineCount]))
    status = proxy.api.getTaskStatus()
    lineCount += 1

# Only want the last line of messages
last=status["message"].splitlines()[-1]

print("\n{}".format(last))

