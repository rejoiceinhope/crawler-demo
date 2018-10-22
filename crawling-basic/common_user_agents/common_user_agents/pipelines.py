# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib

from scrapy.exceptions import DropItem

class DuplicateFilterPipeline(object):
    def __init__(self):
        self.items_seen = set()

    def process_item(self, item, spider):
        fp = hashlib.sha1(item['user_agent_string']).hexdigest()
        if fp in self.items_seen:
            raise DropItem('Duplicate item found: %s' % item['user_agent_string'])
        else:
            self.items_seen.add(item['user_agent_string'])
            return item

class CommonUserAgentsPipeline(object):
    def process_item(self, item, spider):
        return item
