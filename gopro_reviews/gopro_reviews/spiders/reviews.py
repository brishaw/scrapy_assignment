# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['amazon.com']
    start_urls = ["https://www.amazon.com/GoPro-Fusion-Waterproof-Digital-Spherical/product-reviews/B0792MJLNM/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"]

    def parse(self, response):
        ret = response.css('#cm_cr-review_list')
        # collecting star ratings
        starRating = ret.css('.review-rating')
        # collecting titles of each review
        title = ret.css('.review-title')
        # collecting all unique reviews
        uniqeReview = ret.css('.review-text')
        count = 0

        for review in starRating:
            yield{'Stars': ''.join(review.xpath('.//text()').extract()),'Title': ''.join(title.xpath('.//text()').extract()), 'Review': ''.join(uniqeReview[count].xpath(".//text()").extract())}
            count = count + 1
        
        relative_next_url = response.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        yield Request(absolute_next_url, callback=self.parse)
