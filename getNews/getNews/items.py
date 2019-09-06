# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #新闻标题
    title = scrapy.Field()
    #描述
    content = scrapy.Field()
    #新闻日期
    date = scrapy.Field()

class teamItem(scrapy.Item):
    name = scrapy.Field()
    players = scrapy.Field()
