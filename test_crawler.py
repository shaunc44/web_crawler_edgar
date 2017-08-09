import xml.etree.ElementTree as et
tree = et.parse('country_data.xml')
root = tree.getroot()

f = open('output.txt', 'a')

for country in root.findall('country'):
	name = country.get('name')
	rank = country.find('rank').text
	year = country.find('year').text
	gdppc = country.find('gdppc').text
	pop = country[3][0].text

	f.write('%s\t%s\t%s\t%s\t%s\n' % (rank, name, year, gdppc, pop))

f.close()