# import xml.etree.ElementTree as et
# import urllib.request
# import sys

from xml.dom import minidom
import urllib.request as ur


url = 'https://www.sec.gov/Archives/edgar/data/1350694/000114036117019802/form13fInfoTable.xml'
dom = minidom.parse(ur.urlopen(url))
# print ("Dom =", dom)


info_tables = dom.getElementsByTagName('infoTable')
# print ("Root =", root)


output = open('holdings.txt', 'a')


for item in info_tables:
	value = item.getElementsByTagName('value')[0].firstChild.nodeValue
	name = item.getElementsByTagName('nameOfIssuer')[0].firstChild.nodeValue
	# print (value.firstChild.nodeValue)
	# print ("Value =", value)
	# print ("Name =", name)
	shares_node = item.getElementsByTagName('shrsOrPrnAmt')[0]
	shares = shares_node.getElementsByTagName('sshPrnamt')[0].firstChild.nodeValue

	# name = info_table.find('nameOfIssuer').text
	# value = info_table.find('value').text
	# shares = info_table[4][0].text
	output.write('%s\t%s\t%s\n' % (name, value, shares))


output.close()