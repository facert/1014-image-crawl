# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageItem(scrapy.Item):
    image_src = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()


