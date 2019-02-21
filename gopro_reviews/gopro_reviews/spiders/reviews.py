# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from gopro_reviews.items import GoproReviewsItem

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['amazon.com']
    start_urls = ["https://www.amazon.com/GoPro-Fusion-Waterproof-Digital-Spherical/product-reviews/B0792MJLNM/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"]

    def parse(self, response):
        for item in response.css('.a-section.review'):
            if item.css('div::attr(data-hook)').extract_first() == 'review':
                yield {
                        'Review_ID': item.css('div.a-section.celwidget::attr(id)').extract_first().split('-')[1],
                        'Author': item.css('span.a-profile-name::text').extract_first(),
                        'Review': ' '.join(item.css('span.review-text::text').extract())
                        }

        next_page = response.css('.a-last > a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
