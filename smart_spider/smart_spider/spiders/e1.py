import scrapy

class QuotesSpider(scrapy.Spider):
    name = "e1"
    start_urls = [
        'http://homes.e1.ru/kupit/rooms-1,2,3,4,5/?gorod=all&form=11102&zhilaya_novostrojki=1',
    ]


    def parse(self, response):
	with open('i_cucked_your_mommy', 'wb') as f:
	    f.write(response.body)

	for quote in response.css('td.re-search-result-table__body-cell_price'):
	    print quote.css('a::href').extract_first()


