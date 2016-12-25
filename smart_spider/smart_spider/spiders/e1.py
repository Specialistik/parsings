import scrapy
from sqlalchemy import create_engine
#db = create_engine('sqlite:///rooms.db', echo=True)

class PagesSpider(scrapy.Spider):
    name = "e1"
    start_urls = [
        'http://homes.e1.ru/kupit/rooms-1,2,3,4,5/?gorod=all&form=11102&zhilaya_novostrojki=1',
    ]

    def get_rooms_links(self, response):
	for quote in response.css('td.re-search-result-table__body-cell_price'):
	    addiction = self.rooms.insert()
	    addiction.execute(link=quote.css('a').xpath('@href').extract_first(), 	     
	    #print quote.css('a').xpath('@href').extract_first()	


    def parse(self, response):
	base_url = 'http://homes.e1.ru/kupit/rooms-1,2,3,4,5/?gorod=all&form=11102&zhilaya_novostrojki=1&page='
        
	db = create_engine('sqlite:///rooms.db') #, echo=True)
	metadata = BoundMetaData(db)

	self.rooms = Table('rooms', metadata,
    	Column('id', Integer, primary_key=True),
	    Column('link', String(40)),
	    #Column('phone', Integer),
	)
	self.rooms.create()

	#i = users.insert()
	#i.execute(name='Mary', age=30, password='secret')

	last_page = int(response.css('.re-pagination-side-link::text').extract()[-1])
	for page in range(2, 5):  #last_page):
	    yield scrapy.Request(base_url + str(page), callback=self.get_rooms_links)


