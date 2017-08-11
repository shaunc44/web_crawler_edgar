import scrapy
from scrapy.utils.response import open_in_browser

# class SearchEdgar(BaseSpider):
class SearchEdgar(scrapy.Spider):

	name = 'edgar_search'
	start_urls = ['https://www.sec.gov/edgar/searchedgar/companysearch.html']

	def parse(self, response):
		return scrapy.FormRequest.from_response(
			response,
			formid =		'fast-search',
			formdata =		{'CIK': '0001166559'},
			formnumber =	4,
			clickdata =		{'name': 'Find'},
			callback =		self.after,
			method =		'GET'
		)

	def after(self, response):
		# yield Request()
		# print (response.status)

		# if "authentication failed" in response.body:
		# 	self.logger.error("Login failed")
		# 	return
		open_in_browser(response)