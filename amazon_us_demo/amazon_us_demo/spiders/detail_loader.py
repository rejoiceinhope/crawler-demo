# -*- coding: utf-8 -*-

import os
import re
import pdb

import scrapy

from amazon_us_demo.parsers import ProductDetailParser


class DetailLoaderSpider(scrapy.Spider):
    name = 'detail_loader'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/']
    custom_settings = {
        'FIELDS_TO_EXPORT': [
            'asin', 'rank', 'star', 'reviews', 'categories', 'images', 'author',
            'title', 'details', 'feature_bullets', 'book_description', 'product_description'
        ],
        'ITEM_PIPELINES': {
            'amazon_us_demo.pipelines.AmazonUsDetailPipeline': 300
        }
    }

    def start_requests(self):
        asins_path = getattr(self, 'asins_path', None)
        if asins_path is None:
            self.logger.critical(
                '[InvalidArguments] You must supply "asins_path" argument to run detail_loader spider.')
            return

        asins_path = os.path.abspath(os.path.expanduser(asins_path))
        if not os.path.exists(asins_path):
            self.logger.critical('[InvalidArguments] Given "asins_path" does not exist!')
            return

        asin_files = self._find_asin_files(asins_path)
        for asin_file in asin_files:
            with open(asin_file) as asin_fh:
                for line in asin_fh:
                    asin = line.strip()
                    if self._is_valid_asin(asin):
                        yield self._generate_asin_url(asin)

    def parse(self, response):
        try:
            product = ProductDetailParser.parse(response)
            yield product
        except Exception as e:
            self.logger.exception(e)
            pdb.set_trace()

    def _find_asin_files(self, asins_path):
        asin_files = []
        if os.path.isfile(asins_path):
            asin_files.append(asins_path)
            self.logger.debug('[FoundAsinFile] %s', asins_path)
        else:
            for dirpath, dirnames, filenames in os.walk(asins_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    self.logger.debug('[FoundAsinFile] %s', file_path)
                    asin_files.append(file_path)

        return asin_files

    def _is_valid_asin(self, asin):
        valid = bool(
            asin and not asin.isspace() and re.match('[0-9]{9}[0-9Xx]{1}|[A-Z]{1}[0-9A-Z]{9}', asin))
        if not valid:
            self.logger.info('[InvalidASIN] %s', asin)

        return valid

    def _generate_asin_url(self, asin):
        url = 'https://www.amazon.com/dp/' + asin
        referer = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias=aps&field-keywords='
        referer = referer + asin

        return scrapy.Request(url, headers={'Referer': referer})
