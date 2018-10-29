# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import re
import json

class ProductDetailParser(object):
    @classmethod
    def parse(cls, response):
        detail = dict()
        detail['asin'] = cls.parse_asin(response)
        detail['title'] = cls.parse_title(response)
        detail['author'] = cls.parse_author(response)
        detail['feature_bullets'] = cls.parse_feature_bullets(response)
        detail['book_description'] = cls.parse_book_description(response)
        detail['product_description'] = cls.parse_product_description(response)
        detail['images'] = cls.parse_images(response)
        detail['star'] = cls.parse_star(response)
        detail['reviews'] = cls.parse_reviews(response)
        detail['rank'] = cls.parse_rank(response)
        detail['categories'] = cls.parse_categories(response)
        detail['details'] = cls.parse_details(response)

        return detail

    @classmethod
    def parse_author(cls, response):
        author_elems = response.xpath('//*[@id="bylineInfo"]/span[contains(@class, "author")]/a/text()')
        xpath_str = '//*[@id="bylineInfo"]/span[contains(@class, "author")]'
        xpath_str += '//a[contains(@class, "contributorNameID")]/text()'
        author_elems.extend(response.xpath(xpath_str))
        xpath_str = '//*[@id="byline"]/span[contains(@class, "author")]'
        xpath_str += '//a[contains(@class, "contributorNameID")]/text()'
        author_elems.extend(response.xpath(xpath_str))
        xpath_str = '//*[@id="bylineInfo"]/span[contains(@class, "author")]'
        xpath_str += '/a[contains(@class, "a-link-normal")]/text()'
        author_elems.extend(response.xpath(xpath_str))

        return ','.join(author_elems.extract())

    @classmethod
    def parse_title(cls, response):
        raw_title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        return raw_title.strip() if raw_title else ''

    @classmethod
    def parse_asin(cls, response):
        matched = re.match(r'.*www\.amazon\.com\/dp\/([0-9A-Z]{10}).*', response.url)
        return '' if matched is None or len(matched.groups()) <= 0 else matched.groups()[0]

    @classmethod
    def parse_feature_bullets(cls, response):
        return response.xpath(
            '//*[@id="feature-bullets"]/ul/li/span[contains(@class, "a-list-item")]/text()').extract()

    @classmethod
    def parse_book_description(cls, response):
        noscript_elems = response.xpath('//*[@id="bookDescription_feature_div"]/noscript')
        if len(noscript_elems) > 0:
            description = ''.join(noscript_elems.xpath('.//text()').extract()).strip()
        else:
            description = ''

        return description

    @classmethod
    def parse_product_description(cls, response):
        try:
            product_description = ''.join(
                response.xpath('//*[@id="productDescription"]//text()').extract()).strip()
        except:
            product_description = ''

        return product_description

    @classmethod
    def parse_images(cls, response):
        thumb_urls = []

        bottom_thumb_elems = response.xpath('//*[@id="imageBlockThumbs"]//div[contains(@class, "imageThumb")]/img')
        bottom_thumb_urls = bottom_thumb_elems.xpath('./@src').extract()
        thumb_urls.extend(bottom_thumb_urls)

        side_thumb_elems = response.xpath('//*[@id="altImages"]//li[contains(@class, "item")]/img')
        side_thumb_urls = side_thumb_elems.xpath('./@src').extract()
        thumb_urls.extend(side_thumb_urls)

        if len(thumb_urls) <= 0:
            front_img_data = response.xpath('//img[@id="imgBlkFront"]/@data-a-dynamic-image').extract_first()
            if front_img_data:
                try:
                    front_img_dict = json.loads(front_img_data)
                    raw_front_img_urls = front_img_dict.keys()
                    if len(raw_front_img_urls) > 0:
                        thumb_urls.append(raw_front_img_urls.pop(0))
                except:
                    pass

        return thumb_urls

    @classmethod
    def parse_star(cls, response):
        stars = 0
        stars_str = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        try:
            stars = float(stars_str.strip().split().pop(0))
        except:
            pass

        return stars

    @classmethod
    def parse_reviews(cls, response):
        reviews = 0
        reviews_str = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        try:
            reviews = int(reviews_str.strip().split().pop(0))
        except:
            pass

        return reviews

    @classmethod
    def parse_details(cls, response):
        details = dict()

        details_elems = response.xpath(
            '//*[@id="productDetailsTable"]/tr/td/div[@class="content"]/ul/li[not(@id="SalesRank")]')
        for details_elem in details_elems:
            key = details_elem.xpath('./b/text()').extract_first()
            key = key.strip().strip(':') if key else ''
            value = details_elem.xpath('./text()').extract_first()
            value = value.strip() if value else ''
            if key and value:
                details[key] = value

        details_elems = response.xpath(
            '//*[@id="detailBullets_feature_div"]/ul/li/span[@class="a-list-item"]')
        for details_elem in details_elems:
            key = details_elem.xpath('./span[@class="a-text-bold"]/text()').extract_first()
            key = key.strip().strip(':') if key else ''
            value = details_elem.xpath(
                    './span[not(@class="a-text-bold")]/text()').extract_first()
            value = value.strip() if value else ''
            if key and value:
                details[key] = value

        details_elems = response.xpath(
            '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr')
        for details_elem in details_elems:
            key = details_elem.xpath('./th/text()').extract_first()
            key = key.strip().strip(':') if key else ''
            value = details_elem.xpath('./td/text()').extract_first()
            value = value.strip() if value else ''
            if key and value:
                details[key] = value

        return details

    @classmethod
    def parse_specifications(cls, response):
        pass

    @classmethod
    def parse_categories(cls, response):
        category_elems = response.xpath(
            '//*[@id="SalesRank"]/ul[@class="zg_hrsr"]/li[1]/span[@class="zg_hrsr_ladder"]//a')
        if category_elems:
            categories = '>'.join(category_elems.xpath('./text()').extract())
        else:
            xpath_str = '//*[@id="prodDetails"]//table/tbody/tr/'
            common_xpath_str = 'th[contains(@class, "prodDetSectionEntry") and '
            common_xpath_str += 'contains(./text(), "Best Sellers Rank")]'
            common_xpath_str += '/following-sibling::td/span/span[2]/a'
            category_elems = response.xpath(xpath_str + common_xpath_str)

            additional_xpath_str = '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr'
            category_elems.extend(response.xpath(additional_xpath_str + common_xpath_str))

            if category_elems:
                categories = '>'.join(
                    [cs.strip() for cs in category_elems.xpath('./text()').extract()])
            else:
                categories = ''

        return categories

    @classmethod
    def parse_rank(cls, response):
        sales_rank_str = ''.join(response.xpath('//*[@id="SalesRank"]/text()').extract()).strip()
        if sales_rank_str:
            try:
                rank = int(sales_rank_str.split().pop(0).strip('#').replace(',', ''))
            except:
                rank = 0
        else:
            xpath_str = '//*[@id="prodDetails"]//table/tbody/tr/'
            common_xpath_str = 'th[contains(@class, "prodDetSectionEntry") and '
            common_xpath_str += 'contains(./text(), "Best Sellers Rank")]'
            common_xpath_str += '/following-sibling::td/span/span/text()'
            sales_rank_str = ''.join(
                response.xpath(xpath_str + common_xpath_str).extract()).strip()

            additional_xpath_str = '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr'
            sales_rank_str += ''.join(
                response.xpath(additional_xpath_str + common_xpath_str).extract()).strip()
            if sales_rank_str:
                try:
                    rank = int(sales_rank_str.split().pop(0).strip('#').strip(','))
                except:
                    rank = 0
            else:
                rank = 0

        return rank
