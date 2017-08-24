# To crawl the SEC EDGAR website
import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor

# To parse the xml file
from xml.dom import minidom
import urllib.request as ur


class SearchEdgar(scrapy.Spider):

	name = 'edgar_search'

	def __init__(self, cik=None, *args, **kwargs):
		super(SearchEdgar, self).__init__(*args, **kwargs)
		self.start_urls = ['https://www.sec.gov/edgar/searchedgar/companysearch.html']
		self.cik = cik

	#parse() could be removed and then replace the url above with:
	#https://www.sec.gov/cgi-bin/browse-edgar?owner=exclude&action=getcompany&Find=Search&CIK=0001166559
	#and insert the cik code as a variable
	def parse(self, response):
		return scrapy.FormRequest.from_response(
			response,
			formid =		'fast-search',
			formdata =		{'CIK': self.cik},
			formnumber =	4,
			clickdata =		{'name': 'Find'},
			callback =		self.after_search,
			method =		'GET'
		)

	# Follow link that represents the most recent 13F-HR filed
	def after_search(self, response):
		next_page_selector = '//td[text()="13F-HR"]/following-sibling::td/a/@href'
		next_page = response.xpath(next_page_selector).extract_first()
		# print ("Next Page = ", next_page)
		# print ("Next Page TYPE = ", type(next_page))
		return scrapy.Request(
			response.urljoin(next_page),
			callback = self.after_click
		)

	# Follow link of actual xml file containing fund's holdings
	def after_click(self, response1):
		last_page_selector = '//td[text()="2"]/following-sibling::td/following-sibling::td/a[not(contains(@href, "xslForm13F"))]/@href'
		last_page = response1.xpath(last_page_selector).extract_first()
		# print ("Last Page = ", "https://www.sec.gov/" + last_page)
		# print ("Last Page TYPE = ", type(last_page))
		xml_url = "https://www.sec.gov/" + last_page
		self.create_text_from_xml(xml_url)

	# Create text file from xml file
	def create_text_from_xml(self, xml_url):
		dom = minidom.parse(ur.urlopen(xml_url))
		info_tables = dom.getElementsByTagName('infoTable')

		file_name = self.cik

		#Create output file with CIK as the file name
		output = open('%s.txt' % file_name, 'w')
		output.write('%s\t%s\t%s\t%s\n' % ('CompanyName', 'Value(1000s)', 'Shares', 'OrderType'))

		#Iterate through XML file and write pertinent values to text file
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



