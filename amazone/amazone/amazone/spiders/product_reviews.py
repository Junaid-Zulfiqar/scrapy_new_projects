import scrapy
from scrapy_selenium import SeleniumRequest

class ProductReviewsSpider(scrapy.Spider):
    name = 'product_reviews'
    count=1
    # start_urls = [
    #     'https://www.amazon.com/s?k=lighting&page=1'
    #     ]
    # def remove_characters(self, value):
    #     return value.strip('\xa0')
    
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.amazon.com/s?k=lighting&page=1',
            wait_time=3,
            callback=self.parse
        )        

    def parse(self, response):
        products = response.xpath("//span/div/div[@class='a-section a-spacing-medium']")
        for product in products:
            link = product.xpath(".//span/a/@href").get()
            rating = product.xpath(".//div[2]/div[2]/div/span/@aria-label").get()
            rating_split = rating.split(" ")
            value = float(rating_split[0])
            if value > 4.5:
                yield response.follow                                                                                                                                            (url = link, callback = self.parse_details,meta = {"rating":rating})
            else:
                pass    

            # product_url = response.urljoin(link)
            # yield {"product_url":product_url,
            #         "rating":rating}


    def parse_details(self,response):
        rating = response.request.meta['rating']
        title = response.xpath("//span[@id='productTitle']/text()").get()
        title = title.replace("\n","")
        price = response.xpath("//span[@id='priceblock_ourprice']/text()").get()
        global_rating = response.xpath("//span[@id='acrCustomerReviewText']/text()").get()    

        yield {
            "product_rating":rating,
            "product_title":title,
            "product_price":price,
            "global_rating":global_rating
        }    

        # next_page = response.xpath("//li[@class='a-last']/a/@href").get()
        # url_join = response.urljoin(next_page)

        # if next_page:
        #     yield scrapy.Request(url=url_join, callback=self.parse, headers={
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        #     })
            # yield response.follow(url = next_page,callback = self.parse)
            # yield SeleniumRequest(
            #     url=url_join,
            #     wait_time=3,
            #     callback=self.parse
            # )
        ProductReviewsSpider.count+=1
        nxt_page="https://www.amazon.com/s?k=lighting&page="+str(ProductReviewsSpider.count)
        if ProductReviewsSpider.count<7:
            yield response.follow(nxt_page,callback=self.parse)
