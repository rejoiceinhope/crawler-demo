# -*- coding: utf-8 -*-
import pdb
import scrapy


class WhatismybrowserSpider(scrapy.Spider):
    name = 'whatismybrowser'
    allowed_domains = ['developers.whatismybrowser.com']

    def start_requests(self):
        # Only chrome, firefox, opera, safari and internet explorer are supported
        # More browsers could be found at:
        # https://developers.whatismybrowser.com/useragents/explore/software_name/
        common_browsers_links = [
            'https://developers.whatismybrowser.com/useragents/explore/software_name/chrome/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/opera/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/safari/',
            'https://developers.whatismybrowser.com/useragents/explore/software_name/internet-explorer/'
        ]

        for link in common_browsers_links:
            yield scrapy.http.Request(link)

    def parse(self, response):
        max_page = getattr(self, 'max_page', 10)

        ua_elems = response.xpath(
            './/table[contains(@class, "table-useragents")]/tbody/tr/td[contains(@class, "useragent")]/a')
        for ua_elem in ua_elems:
            try:
                ua = ua_elem.xpath('./text()').extract_first().strip()
                self.logger.debug('[UserAgent] %s', ua)
                yield {'user_agent_string': ua.strip('"')}
            except Exception as e:
                self.logger.exception(e)

        next_page_elem = response.xpath(
            './/div[@id="pagination"]/span[contains(@class, "current")]/following-sibling::a')[0]
        if next_page_elem:
            page = int(next_page_elem.xpath('./text()').extract_first().strip())
            if page < max_page:
                next_page_url = next_page_elem.xpath('./@href').extract_first().strip()
                if not next_page_url.startswith('http'):
                    next_page_url = 'https://developers.whatismybrowser.com' + next_page_url
                yield scrapy.http.Request(next_page_url)
