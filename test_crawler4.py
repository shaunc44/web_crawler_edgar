# import xml.etree.ElementTree as et
# import urllib.request
# import sys

from xml.dom import minidom
import urllib.request as ur


url = 'https://www.sec.gov/Archives/edgar/data/1179392/000091957417004235/infotable.xml'
dom = minidom.parse(ur.urlopen(url))
# print ("Dom =", dom)


info_tables = dom.getElementsByTagName('infoTable')
# print ("Root =", root)


#Insert name of hedge fund where holdings file is
output = open('holdings.txt', 'w')
output.write('%s\t%s\t%s\t%s\n' % ('CompanyName', 'Value(1000s)', 'Shares', 'OrderType'))

for item in info_tables:
	name = item.getElementsByTagName('nameOfIssuer')[0].firstChild.nodeValue
	value = item.getElementsByTagName('value')[0].firstChild.nodeValue
	shares_node = item.getElementsByTagName('shrsOrPrnAmt')[0]
	shares = shares_node.getElementsByTagName('sshPrnamt')[0].firstChild.nodeValue
	if item.getElementsByTagName('putCall'):
		put_call = item.getElementsByTagName('putCall')[0].firstChild.nodeValue
	else:
		put_call = 'Market'

	output.write('%s\t%s\t%s\t%s\n' % (name, value, shares, put_call))

output.close()



