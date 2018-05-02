import scrapy
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column


class AvitoSpider(scrapy.Spider):
    name = "avito"

    def __init__(self, **kwargs):
        super(AvitoSpider, self).__init__(**kwargs)
        db = create_engine('sqlite:///avito.db')  # , echo=True)
        metadata = MetaData(db)
        self.last_page_link = None

        self.real_estate = Table('real_estate', metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('link', String(255)),
                                 )

        self.real_estate_base = Table('real_estate_base', metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('link', String(255)),
                                      )
        self.real_estate.create()
        self.real_estate_base.create()

    def start_requests(self):
        base_url = 'https://www.avito.ru/kazan/kvartiry'
        scrapy.Request(url=base_url, callback=self.get_last_page_link)
        proceed_with = 1
        next_url = base_url + '?p=' + str(proceed_with)
        while self.last_page_link != next_url:
            addiction = self.real_estate_base.insert()
            addiction.execute(link=next_url)

            proceed_with += 1
            next_url = base_url + '?p=' + str(proceed_with)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def get_last_page_link(self, response):
        wanted_link = None
        for useless_shit in response.css('a.pagination-page'):
            wanted_link = useless_shit
        self.last_page_link = wanted_link

    def parse(self, response):
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


"""
        last_page = int(response.css('.re-pagination-side-link::text').extract()[-1])
        for page in range(2, last_page):  # last_page):
            yield scrapy.Request(base_url + str(page), callback=self.get_rooms_links)
"""
