# -*- coding: utf-8 -*-

import os
import re

import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

from amazon_page_parser.parsers import OfferListingParser


class OfferListingLoaderSpider(RedisSpider):
    name = 'offer_listing_loader'
    allowed_domains = ['www.amazon.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_us_demo.pipelines.AmazonUsOfferListingPipeline': 300
        },
        'FIELDS_TO_EXPORT': ['asin', 'offers']
    }

    def parse(self, response):
        offer_listings = {
            'asin': self._extract_asin(response)
        }

        parser = OfferListingParser(response.text)
        try:
            offer_listings['offers'] = parser.parse()
            yield offer_listings
        except Exception as e:
            self.logger.exception(e)

    def make_request_from_data(self, data):
        asin = bytes_to_str(data, self.redis_encoding)

        return self._generate_offer_listing_url(asin)

    def _extract_asin(self, response):
        matched = re.match(r'.*www\.amazon\.com\/gp\/offer-listing\/([0-9A-Z]{10}).*', response.url)
        return '' if matched is None or len(matched.groups()) <= 0 else matched.groups()[0]

    def _generate_offer_listing_url(self, asin):
        url = 'https://www.amazon.com/gp/offer-listing/{}'.format(asin)
        referer = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias=aps&field-keywords={}'.format(asin)

        return scrapy.Request(url, headers={'Referer': referer})
