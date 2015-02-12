#!/usr/bin/env python
# (c) Copyright 2014 PaperCut Software International Pty Ltd.
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

HOST = 'localhost'  # The PaperCut server
PORT = 7778         # Default port on PaperCut server for the card reader

userCredentialsDB = {
                        "Alec" : "ed5d34c74e59d16bd",
                        "Chris": "5678",
                        "Julie": "EMP123",
                    }

cardNumber = userCredentialsDB["Alec"]


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
except socket.error, msg:
    print("Socket error on socket.bind {}".format(msg))
    print('could not open socket')
    s.close()
    sys.exit(1)

while 1:
    try:
conn, addr = s.accept()  # Good implementation would only accept from PaperCut server IP
    	print('Connected by', addr)

    	while 1:
        	data = conn.recv(2) # Need to break if error.
        	if not data: continue  #loop around and read again
        	print("Receive data from server {}".format(data))
        	r = "".format(data)
        	if   r == 'v':  # Request for version number
            		conn.send("ExampleVersion 01\n") #PaperCut will log this
        	elif r == 'e':  # Request to flag an error to user (e.g. Unknown card)
            		print("Error Indicator On")   # e.g. flash red LED
        	elif r == 'b':  # Request make a audible indication (may happen multiple times
            		print("Beep sounded")  # on a single card swipe)
        	else:
            		raw_input("Please press enter key to simulate card being swiped")
            		print("Sent card number {}".format(cardNumber))
            		conn.send(cardNumber+'\n')
    except:
    	conn.close()


