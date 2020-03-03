# Creating PaperCut NG top up cards

Using [top up cards](https://www.papercut.com/kb/Main/TopUpCards) is a great "low tech" solution for students to get cash into their PaperCut personal account. PaperCut does supply an MS Word tools to create the import file,
which is designed to work on Windows using MS Office.
You may prefer to create your own tool to generate the cards and the import file.

You'll need to create a process (this may involve creating a small tool) that generates

1. A print file of cards, each of which contains the correct card numbers and other data. These can then be printed and sold to students

2. A data file that has a record for each card you are printing out. This file format is as follows.

File must have the following data encoding
UTF-16 text with MS Windows line endings. The file must have the correct BOM (https://en.wikipedia.org/wiki/Byte_order_mark)

First line is a mandatory header line with the following fixed content

```
CardNumber,BatchID,ValueNumber,Value,ExpDate,ExpDateDisplay
```

Notice. Field Separator is “,”. There are NO quotes around any of the text

Each following data line must look like this

```
"P-1503-BLNZ-YTSF","P-1503","10","$10.00","2015-09-13","13/09/2015"
```

Notice: All fields are text, Field Separator is “,”. Quotes around text are mandatory

The values for the columns "Value" and "ExpDateDisplay" should be in the correct format for your locale

If you want to create a test file manually you can use the following tools
* Libreoffice Spreadsheet can save files as UTF-16  CSV file
* Using an editor such as vim to remove quotes on header line, if you want to get really fancy you can use  a tool such as sed.

If your file is not in MS Windows format use dos2unix tools to create MS Windows format e.g.  unix2dos -f -u -b  file.csv

Once you understand the process then you can consider creating a standalone utility to create batches of cards.
The program [createTopUpCards.py](createTopUpCards.py) is a working exampe of such a utility that
you will need to modify for your locale and requirements.
