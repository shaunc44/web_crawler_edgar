# from __future__ import absolute_import
# from scrapy.spider import BaseSpider
# from scrapy.http import FormRequest, Request
# from scrapy.utils.response import open_in_browser
# from scrapy.selector import HtmlXPathSelector
# from loginform import fill_login_form
import scrapy


# class SearchEdgar(BaseSpider):
class SearchEdgar(scrapy.Spider):

	name = 'search'
	start_url = ['https://www.sec.gov/edgar/searchedgar/companysearch.html']

	def parse(self, response):
		return scrapy.FormRequest.from_response(
			response,
			formname='companySearchForm',
			formid='fast-search',
			formdata={'cik': '1166559'},
			callback=self.after,
			method='GET'
		)

	def after(self, response):
		# yield Request()
		# print (response.status)

		# if "authentication failed" in response.body:
		# 	self.logger.error("Login failed")
		# 	return

		open_in_browser(response)