import scrapy
from web_parser.spiders.utils.types_enum import poem_types
from web_parser.items import ReviewItem


class ReviewSpider(scrapy.Spider):
    name = 'review_spider'
    allowed_domains = ['stihi.ru']

    def start_requests(self):
        for topic in poem_types.keys():
            for year in range(2008, 2022):
                for month in range(1, 13):
                    for day in range(1, 28):
                        for start in range(420, 20, -20):
                            url = (f"https://stihi.ru/board/list.html?"
                                   f"day={day:02d}&"
                                   f"month={month:02d}"
                                   f"&year={year}"
                                   f"&topic={topic}"
                                   f"&start={start}")
                            yield scrapy.Request(url,
                                                 callback=self.parse)

    def parse(self, response, **kwargs):
        selector = '//div[contains(@class, "recstihi")]'
        reviews = response.xpath(selector)
        for review in reviews:
            item = ReviewItem()
            item["poem_url"] = review.xpath(f"{selector}/b/a/@href").extract()
            item["text"] = ''.join(review.xpath(f"{selector}/text()").extract())
            item["author"] = review.xpath(f"{selector}/small/a/text()").extract()
            item["datetime"] = review.xpath(f"{selector}/small/text()").extract()

            yield item