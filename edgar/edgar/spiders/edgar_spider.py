import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.linkextractors import LinkExtractor

# class SearchEdgar(BaseSpider):
class SearchEdgar(scrapy.Spider):

	name = 'edgar_search'
	start_urls = ['https://www.sec.gov/edgar/searchedgar/companysearch.html']

	#This could be removed and the url above replace with:
	#URL =  https://www.sec.gov/cgi-bin/browse-edgar?owner=exclude&action=getcompany&Find=Search&CIK=0001166559
	#and insert the cik code as a variable
	def parse(self, response):
		return scrapy.FormRequest.from_response(
			response,
			formid =		'fast-search',
			formdata =		{'CIK': '0001166559'},
			formnumber =	4,
			clickdata =		{'name': 'Find'},
			callback =		self.after_search,
			method =		'GET'
		)


	def after_search(self, response):
		# yield scrapy.Request(response)
		print ("STATUS = ", response.status)
		print ("Type of response = ", type(response))
		print ("Response = ", response)
		print ("URL = ", response.url)

		# if "authentication failed" in response.body:
		# 	self.logger.error("Login failed")
		# 	return
		# open_in_browser(response)

		#from_response() ????
		link = LinkExtractor(
			response1,
			callback =		self.after_click1,
			follow =		True
		)

		print ("Link = ", link)


	def after_click1(self, response1):
		pass