# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import random
import string

from scrapy import signals
from scrapy.http import FormRequest
from scrapy.exceptions import NotConfigured
from scrapy.exceptions import CloseSpider

from deathbycaptcha.deathbycaptcha import HttpClient


class AmazonUsCaptchaResolverMiddleware(object):
    def __init__(self, username, password, threshold, wait_time, resolve_rate):
        self.username = username
        self.password = password
        self.threshold = threshold
        self.wait_time = wait_time
        self.resolve_rate = resolve_rate

        self.client = HttpClient(username, password)
        self.captcha_stats = {'count': 0, 'first_resolved': None, 'last_resolved': None}

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        if not crawler.settings.getbool('AMAZON_CAPTCHA_RESOLVER_ENABLED'):
            raise NotConfigured()

        username = crawler.settings.get('AMAZON_CAPTCHA_RESOLVER_USERNAME')
        password = crawler.settings.get('AMAZON_CAPTCHA_RESOLVER_PASSWORD')
        threshold = crawler.settings.getint('AMAZON_CAPTCHA_RESOLVER_THRESHOLD', 5)
        wait_time = crawler.settings.getint('AMAZON_CAPTCHA_WAIT_TIME', 3)
        resolve_rate = crawler.settings.getint('AMAZON_CAPTCHA_RESOLVE_RATE', 4)
        if not username or not password:
            raise NotConfigured()

        s = cls(username, password, threshold, wait_time, resolve_rate)

        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        if request.meta.get('proxy', None) is not None:
            return response

        captcha_input = response.xpath('//*[@id="captchacharacters"]').extract_first()
        if captcha_input is not None:
            spider.logger.info('Captcha find, try to resolve it!')

            self.captcha_stats['count'] += 1

            ts = time.time()
            if self.captcha_stats['first_resolved'] is None:
                self.captcha_stats['first_resolved'] = ts
            self.captcha_stats['last_resolved'] = ts

            time_passed = self.captcha_stats['last_resolved'] - self.captcha_stats['first_resolved']
            if time_passed > 0 and self.captcha_stats['count'] / time_passed / 60 > self.threshold:
                self.captcha_stats = {'count': 0, 'last_resolved': None, 'first_resolved': None}
                raise CloseSpider('Too many captcha resolution found')

            time.sleep(self.wait_time)

            captcha_url = response.xpath(
                '//form//div[contains(@class, "a-text-center")]/img/@src').extract_first()
            captcha_text = ''.join(random.sample(string.ascii_lowercase + string.digits, 4))
            if self.captcha_stats['count'] % self.resolve_rate == 0:
                try:
                    r = self.client.upload(captcha_url)
                    if r and 'is_correct' in r and r['is_correct']:
                        captcha_text = self.client.get_text(r['captcha'])
                    else:
                        if r and 'captcha' in r:
                            self.client.report(r['captcha'])
                except:
                    pass

            req = FormRequest.from_response(
                response, formxpath='//form[@action="/errors/validateCaptcha"]',
                formdata={'field-keywords': captcha_text},
                clickdata={'type': 'submit'})
            req.dont_filter = True
            req.meta['proxy'] = None

            return req

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

        return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class AmazonUsDemoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AmazonUsDemoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
