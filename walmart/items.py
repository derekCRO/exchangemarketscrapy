# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WalmartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Marketplace = scrapy.Field()
    ListingTitle = scrapy.Field()
    BusinessName = scrapy.Field()
    AskingPrice = scrapy.Field()
    NetProfit = scrapy.Field()
    GrossRevenue = scrapy.Field()
    Inventory = scrapy.Field()
    averagesales = scrapy.Field()
    sessions = scrapy.Field()
    Description = scrapy.Field()
    BusinessWebsite = scrapy.Field()
    ListingLink = scrapy.Field()
    updatetime=scrapy.Field()
    pass