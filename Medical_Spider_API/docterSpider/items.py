# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DocterspiderItem(scrapy.Item):
    propose = scrapy.Field()
    drugs = scrapy.Field()
    introduce = scrapy.Field()
    Price = scrapy.Field()