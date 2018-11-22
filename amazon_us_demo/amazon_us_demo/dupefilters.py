# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import logging

from scrapy.dupefilters import BaseDupeFilter


logger = logging.getLogger(__name__)

class DummyDupeFilter(BaseDupeFilter):
    logger = logger

    def __init__(self, *args, **kwargs):
        self.debug = kwargs.get('debug', False)
        self.logdupes = True

    @classmethod
    def from_settings(cls, settings):
        debug = settings.getbool('DUPEFILTER_DEBUG')
        return cls(debug=debug)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    @classmethod
    def from_spider(cls, spider):
        return cls.from_settings(spider.settings)

    def request_seen(self, request):
        return False

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
