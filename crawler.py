import urllib.request
import time
from lxml import etree
import datetime as dt
import csv
import sys

today = dt.date.today()
ts = int(time.time()) - 86400
tsend = int(time.time())
report = "url_here".format(ts, tsend)

with urllib.request.urlopen(report) as url:
	soup = url.read()

saveFile = open('{}_report.xml'.format(today), 'wb')
saveFile.write(soup)
saveFile.close()

tree = etree.parse('{}_report.xml'.format(today))
root = tree.getroot()
print (root.tag, root.attrib)

for info_table in root.findall('informationTable'):
	for element in info_table:
		for item in info_table