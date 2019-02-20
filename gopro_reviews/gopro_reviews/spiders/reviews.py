# -*- coding: utf-8 -*-
import scrapy


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['amazon.com']
    productUrl = "https://www.amazon.com/GoPro-Fusion-Waterproof-Digital-Spherical/product-reviews/B0792MJLNM/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber="
    start_urls = []

    # have the spider scrape all of the reviews by concatenating the 'page numbers' to the end of the productUrl.
    # there are 61 reviews, not 61 pages, however, I thought this would guarantee all the reviews.
    for i in range(1, 61):
        start_urls.append(productUrl+str(i))

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
