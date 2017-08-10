# import xml.etree.ElementTree as et
# import urllib.request

import sys
# import lxml
from bs4 import BeautifulSoup
import urllib


xml = urllib.urlopen(
		'https://www.sec.gov/Archives/edgar/data/1350694/000114036117019802/form13fInfoTable.xml'
	).read()

soup = BeautifulSoup(xml, 'lxml-xml')

print ("Soup =", soup)

# tree = et.parse('13f.xml')
# tree = et.parse(urllib.request.urlopen('https://www.sec.gov/Archives/edgar/data/1350694/000114036117019802/form13fInfoTable.xml'))
# root = tree.getroot()
# print ("Root =", root)


# f = open('holdings.txt', 'a')


# for info_table in root.findall('infoTable'):
# 	name = info_table.find('nameOfIssuer').text
# 	value = info_table.find('value').text
# 	shares = info_table[4][0].text

# 	f.write('%s\t%s\t%s\n' % (name, value, shares))

# f.close()