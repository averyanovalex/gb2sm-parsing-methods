# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id =  scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    special_price = scrapy.Field()
    price = scrapy.Field()
    rate = scrapy.Field()
    genre = scrapy.Field()
    annotation = scrapy.Field()
    added_at = scrapy.Field()

