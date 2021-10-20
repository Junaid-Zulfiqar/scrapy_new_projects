import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = 'restaurants'
    allowed_domains = ['www.airbnb.com']
    start_urls = ['http://www.airbnb.com/']

    def parse(self, response):
        pass
