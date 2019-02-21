# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from gopro_reviews.items import GoproReviewsItem

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['amazon.com']
    start_urls = ["https://www.amazon.com/GoPro-Fusion-Waterproof-Digital-Spherical/product-reviews/B0792MJLNM/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"]

    def parse(self, response):
        ret = response.css('#cm_cr-review_list')

        item = GoproReviewsItem()
        # collecting star ratings
        item['starRating'] = ret.css('.review-rating')
        # collecting titles of each review
        item['title'] = ret.css('.review-title')
        # collecting all unique reviews
        item['uniqueReview'] = ret.css('.review-text')
        count = 0

        for review in item['starRating']:
            yield{'Stars': ''.join(review.xpath('.//text()').extract()), 'Title': ''.join(item['title'].xpath('.//text()').extract()), 'Review': ''.join(item['uniqueReview'][count].xpath(".//text()").extract())}
            count = count + 1

        relative_next_url = response.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        yield Request(absolute_next_url, callback=self.parse)
