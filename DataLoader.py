#!/usr/bin/env python
# Coded by Vitali
import urllib
import sqlite3
import re
import pandas as pd

f = urllib.urlopen('CC_20160112_234300.htm')

xdata = f.read()
f.close()

# (1) bin
bin = re.findall(r'<td class="width-50px">(.*)</td><td', xdata)

# (2) card_type
card_type = re.findall(r'="width:50px">(.*)</td><td', xdata)

# (3) processor
#processor = re.findall(r'MASTERCARD|VISA|AMEX', str(data))

# (4) company dirty
company = re.findall(r'<br>(.*)\s</td', xdata)

# (5) zipcode
zipcode = re.findall(r'">([0-9]{5})</td', xdata)
a = open('zipcode.txt', 'w+')
for i in zipcode:
	a.write(i+'\n')

a.close()

# (6) price
price = re.findall(r'<strong>(.{5})</strong>', xdata)

# (7) base
base = re.findall(r'"width-15">([A-Z]{1}.{4,12})', xdata)

# (8) country
country = re.findall(r'(.{4,13})</td><td> ', xdata)

# (9) city
city = re.findall(r' </td><td>(.{3,20})</td><td style="width:70px', xdata)

# (10) expiry
expiry = re.findall(r'<td style="width:50px">(\d{2}\/\d{4})</td>', xdata)

# (11) date
adate = re.findall(r'<span>Date:(.{12,14}),', xdata)

# (12) state 
state = re.findall(r'</td><td>([A-Z ]{4})</td><td>', xdata)

zipped = zip(adate, bin, card_type, company, expiry, zipcode, base, city, state, country, price)
print zipped

conn = sqlite3.connect('CCDatabase.sqlite')
cur = conn.cursor()
conn.text_factory = str
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS DataTable;
CREATE TABLE DataTable (
  id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  adate 			TEXT,
	bin 		  	TEXT,
  card_type   TEXT,
	company 		TEXT,
	expiry			TEXT,
	zipcode			TEXT,
	base			  TEXT,
	city			  TEXT,
	state			  TEXT,
	country			TEXT,
	price 			TEXT
);
''')

for element in zipped:
	adate = element[0]
	bin = element[1]
	card_type = element[2]
	company = element[3]
	expiry = element[4]
	zipcode = element[5]
	base = element[6]
	city = element[7]
	state = element[8]
	country = element[9]
	price = element[10]


	cur.execute('''INSERT OR REPLACE INTO DataTable (adate, bin, card_type, company, expiry, zipcode, base, city, state, country, price) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', ( adate, bin, card_type, company, expiry, zipcode, base, city, state, country, price ) )

conn.commit()

df = pd.read_sql_query("SELECT * FROM CreditCardTable", conn)

print df
print "\n===============================================\n"
print "Run BaseGeoData to map zipcodes to cities."
print "\n===============================================\n"
