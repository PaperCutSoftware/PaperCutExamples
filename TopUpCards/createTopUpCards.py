#!/usr/bin/env python3
# Creates:
#   Print file for cards
#   Import file for PaperCut NG

# For more details about top up cards see https://www.papercut.com/kb/Main/TopUpCards

# Note: Need to install reportlab module


from datetime import date, timedelta
from random import sample
from pdfdocument.document import PDFDocument
import locale

#Modify to suite
locale.setlocale(locale.LC_ALL, '')


template = """
Value: {}

Expiry Date: {}

Batch ID:\t{}
Card ID:\t{:09d}

"""

batchID = input("Please enter the batch ID ")
cardValue = float(input(f'Please enter value to appear on each card '))
numberOfCards = int(input(f'Please enter number of cards to created in batch "{batchID}" '))
expiryDays = int(input("How many days are these cards valid (PaperCut NG will not except these cards after this period)"))


pdf = PDFDocument("printFile.pdf")


pdf.init_report()

# Must be UTF-16 with correct BOM and MD-DOS line endings
importFile = open("importFile", mode="w", newline="\r\n", encoding='utf-16')

# PaperCut needs this header line in this format
importFile.write("CardNumber,BatchID,ValueNumber,Value,ExpDate,ExpDateDisplay\n")

# Modify to as needed
expDate = date.today() + timedelta(days=14) # expire all the cards in two weeks

displayValue = locale.currency( cardValue, grouping=True )

displayExpDate = expDate.strftime("%x")

isoExpDate = expDate.isoformat()

for cardNumber in sample(range(100000000), numberOfCards):

    importFile.write(
        f'"{batchID}-{cardNumber:09d}","{batchID}","{cardValue}","{displayValue}","{isoExpDate}","{displayExpDate}"\n')

    pdf.start_keeptogether(); # Make sure cards are not split across page boundaries
    pdf.h1("PaperCut NG Top Up Card")
    pdf.p(template.format(displayValue,  displayExpDate,  batchID, cardNumber))
    pdf.end_keeptogether()

pdf.generate()
importFile.close()
