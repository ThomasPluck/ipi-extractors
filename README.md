# ipi-extractors

Run `pip install -r requirements.txt` to install required libraries

You can then run with `python3 page2table.py`, specifically designed for B&A reports which works with the following commands:

`Enter relative path to PDF: `, give relative path from script to your PDF report.

`Enter table PDF page number: `, give page number of table in report to be extracted

The table is then copied to the clipboard and can be directly pasted into either excel or google sheets.

Some extra things that are worth knowing:

  - Entering `,` after your page number will cause the program to drop the indexing and total columns
  - Entering `x` in page number will return you to the previous prompt the program asks you for a PDF path
