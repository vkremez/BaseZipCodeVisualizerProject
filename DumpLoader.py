#!/usr/bin/env python
# Coded by Vitali
import sqlite3
import re
import pandas as pd
f = open('alldumps.htm', 'r+')
# bin,card,Debit/Credit, Mark, Expires, Country, State, City, Zip, Phone, Base, Price
# bin = []
#company = []
# card_type = []
# expiry = []
# country = []
# state = []
# city = []
# zipcode = []
# base = []
# price = []
# adate = []
#processor = []

#data = f.read().split('>')
xdata = f.read()
f.close()

# (1) bin 
bin = re.findall(r'<td class="width-50px">(.*)</td><td', xdata)

# (2) card_type 
card_type = re.findall(r'="width:50px">([A-Z]{5,10})</td><td', xdata)

# (3) processor
processor = re.findall(r'(MASTERCARD </td><td style=|VISA </td><td style=|AMEX </td><td style=)', xdata)

# (4) company
company = re.findall(r'<td style="width:100px">([A-Z\D\-\.0-9]{0,120})</td><td class="width-15', xdata)

# (5) mark
mark = re.findall(r'</td><td style="width:100px">([A-Z\D-]{4,15})</td>', xdata)

# (6) price
price = re.findall(r'<strong>(.{1,7})\$</strong>', xdata)

# (7) base 
base = re.findall(r'"width-15">([A-Z]{1}.{4,20})', xdata)

# (8) country 
country = re.findall(r'style="margin-top:3px">(.{4,45})', xdata)

# (9) code  
code = re.findall(r'<td class="width-10">(.{3,5})</td>', xdata)

# (10) expiry 
expiry = re.findall(r'<td style="width:50px">([0-9/-]{2,5})</td><td', xdata)

# (11) date
adate = re.findall(r'<span>Date:(.{12,14}),', xdata)


zipped = zip(adate, bin, processor, card_type, company, mark, expiry, base, country, price)

conn = sqlite3.connect('DumpShopTable.sqlite')
cur = conn.cursor()
conn.text_factory = str
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS DumpTable;
CREATE TABLE DumpTable (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    adate 			TEXT,
	bin 			TEXT,
    processor    	TEXT,
	card_type 		TEXT,
	company			TEXT,
	mark			TEXT,
	expiry			TEXT,
	base			TEXT,
	country			TEXT,
	price 			FLOAT
);
''')

for element in zipped:
	adate = element[0]
	bin = element[1]
	processor = element[2]
	card_type = element[3]
	company = element[4]
	mark = element[5]
	expiry = element[6]
	base = element[7]
	country = element[8]
	price = element[9]

	cur.execute('''INSERT OR REPLACE INTO DumpTable (adate, bin, processor, card_type, company, mark, expiry, base, country, price) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', ( adate, bin, processor, card_type, company, mark, expiry, base, country, price ) )

conn.commit()

df = pd.read_sql_query("SELECT * FROM DumpTable", conn)

print df
print "\n===============================================\n"
print "Run BaseGeoData to map zipcodes to cities."
print "\n===============================================\n"
