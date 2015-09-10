# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapycustomdownloaderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    memprice = scrapy.Field()
    press = scrapy.Field()
    publication = scrapy.Field()
    author = scrapy.Field()
    desc = scrapy.Field()
    belong = scrapy.Field()

    pass
