import scrapy


class ProductReviewsSpider(scrapy.Spider):
    name = 'product_reviews'
    allowed_domains = ['www.amazon.com']

    def start_requests(self):
        yield scrapy.Request(url='https://www.amazon.com/s?k=lighting/', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
        })

    def parse(self, response):
        products = response.xpath("//span/div/div[@class='a-section a-spacing-medium']")
        for product in products:
            link = product.xpath(".//span/a/@href").get()
            rating = product.xpath(".//div[2]/div[2]/div/span/@aria-label").get()
            rating_split = rating.split(" ")
            value = float(rating_split[0])
            if value > 4.5:
                yield response.follow(url = link, callback = self.parse_details,meta = {"rating":rating})
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

        # if url_join:
        #     yield scrapy.Request(url=next_page, callback=self.parse, headers={
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        #     })