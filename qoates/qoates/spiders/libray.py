import scrapy
import json
from scrapy.exceptions import CloseSpider




class LibraySpider(scrapy.Spider):
    name = 'library'
    allowed_domains = ['openlibrary.org']

    incremented_by = 12
    offset = 0
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12&offset=12']

    def parse(self, response):
        if response.status == 500:
            return CloseSpider("reached last page .....")
        resp = json.loads(response.body)
        works = resp.get('works')
        for count in works:
           yield {
               "title":count.get("title"),
               "subject":count.get("subject")
           }
        self.offset +=self.incremented_by   
        yield scrapy.Request(url = f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}',callback = self.parse)
