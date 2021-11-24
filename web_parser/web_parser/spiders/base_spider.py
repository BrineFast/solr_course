import logging

import scrapy

logging.getLogger('scrapy').setLevel(logging.ERROR)

class BaseSpiderSpider(scrapy.Spider):
    name = 'base_spider'
    allowed_domains = ['www.citilink.ru']
    start_urls = ['https://www.citilink.ru/catalog/naushniki/']
    pages_count = 10

    def start_requests(self):
        types = ["naushniki", "smartfony"]
        for type in types:
            for page in range(1, 2):
                url = f"https://www.citilink.ru/catalog/{type}/?p={page}"
                yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        selector_horizontal = '//div[contains(@class, "ProductCardHorizontal__header-block")]/a/@href'
        selector_vertical = '//div[contains(@class, "ProductCardVerticalLayout__header")]/div/a/@href'
        for href in response.xpath(selector_horizontal).extract() or response.xpath(selector_vertical).extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        print(response.url)


