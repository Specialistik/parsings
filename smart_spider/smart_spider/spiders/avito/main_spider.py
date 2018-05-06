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
        base_ajax_url = 'https://www.avito.ru/items/phone/%s?pkey=%s&vsrc=r'
        for link_raw in response.css('a.item-description-title-link'):
            link = link_raw.css('a').xpath('@href').extract_first()
            addiction = self.real_estate.insert()
            addiction.execute(link=link)

            ad_id = link.split('_')[-1]
            real_ajax_link = base_ajax_url + ad_id + '/'

            # "a.button item-phone-button js-item-phone-button item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card"
            # https://www.avito.ru/items/phone/1300276049?pkey=a9aeff83e06e4218730c5da4062b0250&vsrc=r
            ajax_idea = link_raw.css('a.item-phone-button').xpath()
            scrapy.Request()

