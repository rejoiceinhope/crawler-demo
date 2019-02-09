# -*- coding: utf-8 -*-

import os
import re

import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

from amazon_page_parser.parsers import DetailParser


class DetailLoaderSpider(RedisSpider):
    name = 'detail_loader'
    allowed_domains = ['www.amazon.com']
    custom_settings = {
        'FIELDS_TO_EXPORT': [
            'asin', 'rank', 'star', 'reviews', 'categories', 'images', 'author',
            'title', 'details', 'feature_bullets', 'book_description', 'product_description'
        ],
        'ITEM_PIPELINES': {
            'amazon_us_demo.pipelines.AmazonUsDetailPipeline': 300
        }
    }

    def parse(self, response):
        parser = DetailParser(response.text)
        try:
            info = parser.parse()
            info['asin'] = self._extract_asin(response)
            yield info
        except Exception as e:
            self.logger.exception(e)

    def _extract_asin(self, response):
        matched = re.match(r'.*www\.amazon\.com\/dp\/([0-9A-Z]{10}).*', response.url)
        return '' if matched is None or len(matched.groups()) <= 0 else matched.groups()[0]

    def make_request_from_data(self, data):
        asin = bytes_to_str(data, self.redis_encoding)

        return self._generate_asin_url(asin)

    def _generate_asin_url(self, asin):
        url = 'https://www.amazon.com/dp/' + asin
        referer = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias=aps&field-keywords='
        referer = referer + asin

        return scrapy.Request(url, headers={'Referer': referer})
