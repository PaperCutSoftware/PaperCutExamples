#!/usr/bin/env python3
# Creates:
#   Print file for cards
#   Import file for PaperCut NG

# For more details about top up cards see https://www.papercut.com/kb/Main/TopUpCards

# Need to unstall reportlab module

import locale
locale.setlocale(locale.LC_ALL, '')
from datetime import date, timedelta
from random import sample
from pdfdocument.document import PDFDocument

template = """
Value: {}

Expiry Date: {}

Batch ID:\t{}
Card ID:\t{:09d}

"""
batchID = input("Please enter batch ID ")
cardValue = float(input(f'Please enter value to appear on each card '))
numberOfCards = int(input(f'Please enter number of cards to created in batch "{batchID}" '))
pdf = PDFDocument("printFile.pdf")
pdf.init_report()

# Must be UTF-16 with correct BOM and MD-DOS line endings
importFile = open("importFile", mode="w", newline="\r\n", encoding='utf-16')

# PaperCut needs this header line in this format
importFile.write("CardNumber,BatchID,ValueNumber,Value,ExpDate,ExpDateDisplay\n")

expDate = date.today() + timedelta(days=14) # expire all the cards in two weeks

for cardNumber in sample(range(100000000), numberOfCards):

    importFile.write('"{0}-{1:09d}","{0}","{2}","{3}","{4}","{5}"\n'.format(
                batchID, cardNumber, cardValue, locale.currency( cardValue, grouping=True ), expDate.isoformat(), expDate.strftime("%x")))

    pdf.start_keeptogether(); # Make sure cards are not split across page boundaries
    pdf.h1("PaperCut Top Up Card")
    pdf.p(template.format(locale.currency( cardValue, grouping=True ),  expDate.strftime("%x"),  batchID, cardNumber))
    pdf.end_keeptogether()

pdf.generate()
importFile.close()
