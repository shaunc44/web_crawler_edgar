import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor
from xml.dom import minidom
import urllib.request as ur


class SearchEdgar(scrapy.Spider):

	name = 'edgar_search'
	start_urls = ['https://www.sec.gov/edgar/searchedgar/companysearch.html']

	#This could be removed and the replace url above with:
	#URL =  https://www.sec.gov/cgi-bin/browse-edgar?owner=exclude&action=getcompany&Find=Search&CIK=0001166559
	#and insert the cik code as a variable
	def parse(self, response):
		return scrapy.FormRequest.from_response(
			response,
			formid =		'fast-search',
			formdata =		{'CIK': '0001350694'},
			formnumber =	4,
			clickdata =		{'name': 'Find'},
			callback =		self.after_search,
			method =		'GET'
		)


	def after_search(self, response):
		next_page_selector = '//td[text()="13F-HR"]/following-sibling::td/a/@href'
		next_page = response.xpath(next_page_selector).extract_first()
		print ("Next Page = ", next_page)
		print ("Next Page TYPE = ", type(next_page))
		return scrapy.Request(
			response.urljoin(next_page),
			callback=self.after_click
		)


	def after_click(self, response1):
		# last_page_selector = '//td[text()="2"]/following-sibling::td/following-sibling::td/a[not(contains(@href, "xsl"))]'
		last_page_selector = '//td[text()="2"]/following-sibling::td/following-sibling::td/a[not(contains(@href, "xslForm13F"))]/@href'
		last_page = response1.xpath(last_page_selector).extract_first()
		print ("Last Page = ", "https://www.sec.gov/" + last_page)
		print ("Last Page TYPE = ", type(last_page))

		xml_url = "https://www.sec.gov/" + last_page
		# return "https://www.sec.gov/" + last_page
		self.create_text_from_xml(xml_url)
		# return xml_url
		# return scrapy.Request(
		# 	response.urljoin(next_page),
		# 	callback=self.create_text_from_xml
		# )


	def create_text_from_xml(self, xml_url):
		# url = 'https://www.sec.gov/Archives/edgar/data/1062589/000090266417001168/infotable.xml'
		# dom = minidom.parse(ur.urlopen(url))
		print ("YOU ARE IN THE CREATE TEXT FUNCTION")
		dom = minidom.parse(ur.urlopen(xml_url))
		info_tables = dom.getElementsByTagName('infoTable')


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


		# if "authentication failed" in response.body:
		# 	self.logger.error("Login failed")
		# 	return
		# open_in_browser(next_page)
		# response.urljoin(next_page)

		#from_response() ????
		# link = LinkExtractor(
		# 	# response,
		# 	# allow =				(),
		# 	restrict_css =		'.tableFile2 .blueRow td="13F-HR" a ::attr(href)'
		# 	# callback =			self.after_click1,
		# 	# follow =			True
		# )

		# print ("Link = ", link)










