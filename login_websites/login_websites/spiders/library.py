import scrapy
from scrapy import FormRequest

class LibrarySpider(scrapy.Spider):
    name = 'library'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/account/login']

    def parse(self, response):
        yield FormRequest.from_response(
            response,
            formid = "register",
             formdata = {
                "username": "nayabvector@gmail.com",
                "password": "149092",
                "redirect":"https://openlibrary.org/",
                "debug_token": "",
                "login": "Log In"
               },
         callback =  self.login_data
        )

    def login_data(self,response):
        if response.xpath("//form[@action='/account/logout']/button/text()").get():
            print("login in ............")

