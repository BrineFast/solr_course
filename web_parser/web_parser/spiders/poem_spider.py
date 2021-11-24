import scrapy

from web_parser.spiders.utils.types_enum import poem_types

from web_parser.items import PoemItem


class PoemSpider(scrapy.Spider):
    name = 'poem_spider'
    allowed_domains = ['stihi.ru']

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5
    }

    def start_requests(self):
        for topic in poem_types.keys():
            for year in range(2017, 2021):
                for month in range(2, 3):
                    for day in range(1, 28):
                        for start in range(500, 20, -20):
                            url = (f"https://stihi.ru/poems/list.html?"
                                   f"day={day:02d}&"
                                   f"month={month:02d}"
                                   f"&year={year}"
                                   f"&topic={topic}"
                                   f"&start={start}")
                            yield scrapy.Request(url,
                                                 callback=self.parse_pages,
                                                 cb_kwargs=dict(date=f'{day}-{month}-{year}',
                                                                topic=topic))

    def parse_pages(self, response, **kwargs):
        selector = '//a[contains(@class, "poemlink")]/@href'
        for href in response.xpath(selector).extract():
            url = response.urljoin(href)
            print(url)
            yield scrapy.Request(url,
                                 callback=self.parse,
                                 cb_kwargs=dict(date=kwargs["date"],
                                                topic=kwargs["topic"]))

    def parse(self, response, **kwargs):
        item = PoemItem()
        item["topic"] = response.xpath('//div[@class="maintext"]/index/h1/text()').extract_first()
        item["author"] = response.xpath('//div[@class="titleauthor"]/em/a/text()').extract_first()
        item["text"] = ''.join(response.xpath('//div[@class="text"]/text()').extract())
        item["date"] = kwargs["date"]
        item["topic"] = poem_types[kwargs["topic"]]

        yield item


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    process.crawl(PoemSpider)
    process.start()
