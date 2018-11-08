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


class OfferListingParser(object):

    @classmethod
    def parse(cls, response):
        offers = []
        asin = cls.parse_asin(response)
        for offer_elem in response.xpath('.//div[@id="olpOfferList"]//div[contains(@class, "olpOffer")]'):
            offer = dict()
            offer['price'] = cls.parse_price(offer_elem)
            offer['shipping_price'] = cls.parse_shipping_price(offer_elem)
            offer['condition'], offer['subcondition'] = cls.parse_condition(offer_elem)
            offer['condition_comments'] = cls.parse_condition_comments(offer_elem)
            offer['available'] = cls.parse_availability(offer_elem)
            offer['prime'] = cls.parse_prime(offer_elem)
            offer['expected_shipping'] = cls.parse_expected_shipping(offer_elem)
            offer['seller_name'] = cls.parse_seller_name(offer_elem)
            offer['seller_rating'] = cls.parse_seller_rating(offer_elem)
            offer['seller_feedbacks'] = cls.parse_seller_feedbacks(offer_elem)
            offer['seller_stars'] = cls.parse_seller_stars(offer_elem)
            offer['offer_listing_id'] = cls.parse_offer_listing_id(offer_elem)
            offers.append(offer)

        return {'asin': asin, 'offers': json.dumps(offers)}

    @classmethod
    def parse_asin(cls, response):
        matched = re.match(r'.*www\.amazon\.com\/gp\/offer-listing\/([0-9A-Z]{10}).*', response.url)
        return '' if matched is None or len(matched.groups()) <= 0 else matched.groups()[0]

    @classmethod
    def parse_price(cls, offer_elem):
        price = 0

        price_str = offer_elem.xpath(
            './div[contains(@class, "olpPriceColumn")]/span[contains(@class, "olpOfferPrice")]/text()').extract_first()
        if price_str:
            price = float(re.sub(r'[^0-9\.]', '', price_str.strip().replace(',', '.')))
        else:
            raise RuntimeError('Could not find price element')

        return price

    @classmethod
    def parse_shipping_price(cls, offer_elem):
        shipping_price = 0

        prime_elem = offer_elem.xpath(
            './div[contains(@class, "olpPriceColumn")]/span[contains(@class, "supersaver")]').extract_first()
        if prime_elem:
            return 0

        shipping_price_str = offer_elem.xpath(
            './div[contains(@class, "olpPriceColumn")]/p[@class="olpShippingInfo"]//span[@class="olpShippingPrice"]/text()').extract_first()
        if shipping_price_str:
            return float(shipping_price_str.strip().replace('$', '').replace(',', ''))

        free_shipping_str = offer_elem.xpath(
            './div[contains(@class, "olpPriceColumn")]/p[@class="olpShippingInfo"]/span[@class="a-color-secondary"]/b/text()').extract_first()
        if free_shipping_str:
            if free_shipping_str.lower().find('free') != -1:
                return 0

        raise RuntimeError('Could not find shipping price element')

    @classmethod
    def parse_condition(cls, offer_elem):
        condition = ''
        sub_condition = ''

        condition_elem = offer_elem.xpath(
            './div[contains(@class, "olpConditionColumn")]//span[contains(@class, "olpCondition")]')
        if not condition_elem:
            raise RuntimeError('Could not find condition element')

        id_str = condition_elem.xpath('./@id').extract_first()
        if id_str:
            if id_str.lower().find('new') != -1:
                condition = 'New'
                sub_condition = 'New'
            elif id_str.lower().find('collectible') != -1:
                condition = 'Collectible'
                sub_condition = condition_elem.xpath(
                    './span[@id="offerSubCondition"]/text()').extract_first().strip()
            else:
                condition = 'Used'
                sub_condition = condition_elem.xpath(
                    './span[@id="offerSubCondition"]/text()').extract_first().strip()
        else:
            condition_strs = condition_elem.xpath('.//text()').extract()
            condition_str = [part.strip() for part in condition_strs]
            if condition_str.lower().find('new') != -1:
                condition = 'New'
                sub_condition = 'New'
            elif condition_str.lower().find('collectible') != -1:
                condition = 'Collectible'
                sub_condition = condition_elem.xpath(
                    './span[@id="offerSubCondition"]/text()').extract_first().strip()
            else:
                conditions = [part.strip() for part in condition_str.split('-')]
                if len(conditions) > 1:
                    condition = conditions.pop(0)
                    sub_condition = conditions.pop(0)
                else:
                    condition = conditions.pop(0)
                    sub_condition = condition

        return (condition, sub_condition)

    @classmethod
    def parse_condition_comments(cls, offer_elem):
        comments = ''

        comments_elem = offer_elem.xpath(
            './div[contains(@class, "olpConditionColumn")]/div[contains(@class, "comments")]')
        if comments_elem:
            comments_wrappers = comments_elem.xpath('.//div')
            if len(comments_wrappers) > 0:
                comment_strs = comments_wrappers.xpath('./text()').extract()
                comments = ''.join([comment_str.strip() for comment_str in comment_strs])
            else:
                comments = comments_elem.xpath('./text()').extract_first().strip()

        return comments

    @classmethod
    def parse_availability(cls, offer_elem):
        available = True

        availability_elem = offer_elem.xpath(
            './olpAvailability').extract_first()
        if availability_elem:
            availability_str = availability_elem.xpath('./text()').extract_first().strip()
            if availability_str:
                available = False

        return available

    @classmethod
    def parse_prime(cls, offer_elem):
        prime_elem = offer_elem.xpath(
            './div[contains(@class, "olpPriceColumn")]/span[contains(@class, "supersaver")]').extract_first()
        return prime_elem is not None

    @classmethod
    def parse_expected_shipping(cls, offer_elem):
        shipping_content = ''.join(offer_elem.xpath(
            './div[contains(@class, "olpDeliveryColumn")]/ul[contains(@class, "olpFastTrack")]/li//text()').extract())
        expected_shipping = bool(
            re.search(r'.*(One|Two)-Day Shipping.*', shipping_content, re.M))
        expected_shipping = expected_shipping or bool(
            re.search(r'.*Expedited Shipping.*', shipping_content, re.M))
        return expected_shipping

    @classmethod
    def parse_seller_name(cls, offer_elem):
        seller_name = ''

        amazon_elem = offer_elem.xpath(
            './div[contains(@class, "olpSellerColumn")]/*[contains(@class, "olpSellerName")]//img').extract_first()
        if amazon_elem is not None:
            return 'Amazon'

        raw_seller_name = offer_elem.xpath(
            './div[contains(@class, "olpSellerColumn")]/*[contains(@class, "olpSellerName")]//a/text()').extract_first()
        if raw_seller_name:
            seller_name = raw_seller_name.strip()
        else:
            raise RuntimeError('Could not find seller name')

        return seller_name

    @classmethod
    def parse_seller_rating(cls, offer_elem):
        rating = 0

        rating_str = offer_elem.xpath(
            './div[contains(@class, "olpSellerColumn")]/p/a/b/text()').extract_first()
        if rating_str:
            rating = int(rating_str.split().pop(0).replace('%', ''))
        else:
            rating = 0

        return rating

    @classmethod
    def parse_seller_feedbacks(cls, offer_elem):
        feedbacks = 0

        seller_desc_elem = offer_elem.xpath(
            './div[contains(@class, "olpSellerColumn")]/p')
        if seller_desc_elem:
            raw_seller_descs = seller_desc_elem.xpath('./text()').extract()
            seller_desc = ''.join([raw_seller_desc.strip() for raw_seller_desc in raw_seller_descs])
            if seller_desc:
                matched_feedback = re.match(r'.*\(([0-9\.,]+) total ratings\)', seller_desc)
                raw_feedbacks_str = matched_feedback.groups()[0] if matched_feedback and len(matched_feedback.groups()) > 0 else '0'
                feedbacks = int(raw_feedbacks_str.replace(',', ''))
            else:
                feedbacks = 0

        return feedbacks

    @classmethod
    def parse_seller_stars(cls, offer_elem):
        star = 0

        raw_star_str = offer_elem.xpath(
            './div[contains(@class, "olpSellerColumn")]/p/i/span/text()').extract_first()
        if raw_star_str:
            star = float(raw_star_str.split().pop(0))
        else:
            star = 0

        return star

    @classmethod
    def parse_offer_listing_id(cls, offer_elem):
        return offer_elem.xpath(
            './div[contains(@class, "olpBuyColumn")]//form/input[@name="offeringID.1"]/@value').extract_first()
