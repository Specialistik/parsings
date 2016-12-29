import scrapy
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column

class RoomsSpider(scrapy.Spider):
    name = "rooms"

    def __init__(self, *args, **kwargs):
		super(RoomsSpider, self).__init__(*args, **kwargs)
		
		db = create_engine('sqlite:///rooms.db') #, echo=True)
		metadata = MetaData(db)
		self.rooms = Table('rooms', metadata, autoload=True)
		r = self.rooms.select()
		rs = r.execute()
		for phone_page in rs:
			self.start_urls.append(phone_page.link)

    def get_phone(self, response):
		phone_ajax_link = response.css('#show_phone').xpath('@data-link').extract_first()

    def get_rooms_links(self, response):
		for quote in response.css('td.re-search-result-table__body-cell_price'):
		    addiction = self.rooms.insert()
		    addiction.execute(link=quote.css('a').xpath('@href').extract_first())

    def parse(self, response):
		phone_ajax_link = response.css('#show_phone').xpath('@data-link').extract_first()
		print phone_ajax_link
