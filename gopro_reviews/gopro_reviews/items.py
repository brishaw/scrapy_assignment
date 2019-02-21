# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# import scrapy

# class GoproReviewsItem(scrapy.Item):
#     pass

import scrapy
from scrapy.item import Item, Field

class GoproReviewsItem(Item):
    starRating = Field()
    title = Field()
    uniqueReview = Field()
