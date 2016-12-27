import scrapy
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column

class PagesSpider(scrapy.Spider):
    name = "rooms"

    def __init__(self, *args, **kwargs):
	super(PagesSpider, self).__init__(*args, **kwargs)
	db = create_engine('sqlite:///rooms.db') #, echo=True)
	metadata = MetaData(db)
	self.rooms = Table('rooms', metadata, autoload=True)
	r = self.rooms.select()
	rs = r.execute()
	for phone_page in rs:
	    start_urls.append(phone.page.link)

    def get_phone(self, response):
		phone_ajax_link = response.css('#show_phone').xpath('@data-link').extract_first()

    def get_rooms_links(self, response):
		for quote in response.css('td.re-search-result-table__body-cell_price'):
		    addiction = self.rooms.insert()
		    addiction.execute(link=quote.css('a').xpath('@href').extract_first())

    def parse(self, response):
	# continue here
	ajax_phone = response.css()
	# from start_urls response comes
		#for page in range(2, last_page):  #last_page):
		#    yield scrapy.Request(base_url + str(page), callback=self.get_rooms_links)


