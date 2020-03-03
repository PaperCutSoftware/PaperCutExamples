#!/usr/bin/env python
# (c) Copyright 2014-15 PaperCut Software International Pty Ltd.
#
# An example Python script demonstrating how to implement the Card Reader Fast Release
# protocol for PaperCut

# Setup: In the PaperCut Admin interface setup a supported MFD device with
# a network card reader. A fast release terminal may be used instead

# Note that this is an example implementation only and not intended for
# production use. Please consult the PaperCut Knowledge Base or contact
# PaperCut support for assistance

import socket
import sys

HOST = "0.0.0.0"  # Bind on any address
PORT =  7778      # Default port on PaperCut server for the card reader


# Some example accounts
userCredentialsDB = {
                        "Alec" : "ed5d34c74e59d16bd",
                        "Chris": "5678",
                        "Julie": "EMP123",
                    }

cardNumber = userCredentialsDB["Alec"]  # Change to suite


versionString = "Custom Python Script"


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    print("Returned from socket creation")
    s.bind((HOST, PORT))
#    print("Returned from bind")
    s.listen(1)
#    print("Returned from listen")
except socket.error, msg:
    print("Socket error on socket.bind {}".format(msg))
    print('could not open socket')
    s.close()
    sys.exit(1)


try:
    conn, addr = s.accept()  # Good implementation would only accept from PaperCut server IP
    print('Connected by', addr)

    data = conn.recv(50) # Throw '\r' away
    print("I got \"{}\". Will Throw away".format(repr(data)))
    data = conn.recv(50) # Throw rfid prompt away away
    print("I got \"{}\". Will Throw away".format(repr(data)))

except:
    conn.close()
    print("Error in connection attempt")

while 1:

    data = conn.recv(50).rstrip() # throw away trailing whitepace
    if not data: #  We got a reset. Send a card number
        raw_input("Please press enter key to simulate card being swiped")
        print("Sending card number \"{}\"".format(cardNumber))
        conn.send(cardNumber+'\n')
    else:
        r = data[-1] # get last command char
        print("Received command from server \"{}\"".format(r))

        if   r == 'v':  # Request for version number
            conn.send("{}\r".format(versionString)) #PaperCut will log this
            print("Sent version string \"{}\"".format(versionString))
        elif r == 'e':  # Request to flag an error to user (e.g. Unknown card)
            print("Error Indicator On")   # e.g. flash red LED
        elif r == 'b':  # Request make a audible indication (may happen multiple times
            print("Beep sounded")  # on a single card swipe)
# Endwhile

conn.close()


