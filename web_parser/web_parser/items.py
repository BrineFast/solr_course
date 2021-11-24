import scrapy


class PoemItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
    topic = scrapy.Field()

class ReviewItem(scrapy.Item):
    poem_url = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    datetime = scrapy.Field()