import scrapy
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print BASE_DIR

class AvitoSpider(scrapy.Spider):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db = create_engine('sqlite:///real_estate.db')  # , echo=True)
        metadata = MetaData(db)

        self.real_estate = Table('real_estate', metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('link', String(40)),
                                 )
        self.real_estate.create()

    name = "avito"
    start_urls = [
        'https://www.avito.ru/kazan/nedvizhimost',
    ]

    def get_pages(self, response):
        for link in response.css('a.item-description-title-link'):
            addiction = self.real_estate.insert()
            addiction.execute(link=link.css('a').xpath('@href').extract_first())
        # phone_ajax_link = response.css('#show_phone').xpath('@data-link').extract_first()

    """
        def get_rooms_links(self, response):
            for quote in response.css('td.re-search-result-table__body-cell_price'):
                addiction = self.rooms.insert()
                addiction.execute(link=quote.css('a').xpath('@href').extract_first())
    """

    def parse(self, response):
        print 'aa'
        base_url = 'https://www.avito.ru/kazan/nedvizhimost'
        scrapy.Request(base_url, callback=self.get_pages)


"""
        last_page = int(response.css('.re-pagination-side-link::text').extract()[-1])
        for page in range(2, last_page):  # last_page):
            yield scrapy.Request(base_url + str(page), callback=self.get_rooms_links)
"""
