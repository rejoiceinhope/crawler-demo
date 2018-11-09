# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import types
import logging
from datetime import datetime

from scrapy.exceptions import DropItem

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch.exceptions import RequestError
from elasticsearch.exceptions import ConnectionTimeout
from elasticsearch.exceptions import ConnectionError
from elasticsearch.exceptions import SSLError
from elasticsearch.exceptions import TransportError


def format_detail(item):
    formatted_item = dict()
    formatted_item['asin'] = item['asin']
    formatted_item['title'] = item['title']
    formatted_item['author'] = item['author']
    feature_bullets = [f_bullet.strip().replace('\n', '<br />').replace('\t', ' ') for f_bullet in item['feature_bullets']]
    formatted_item['feature_bullets'] = '#FeatureBullets#'.join(feature_bullets)
    formatted_item['book_description'] = item['book_description'].replace('\n', '<br />').replace('\t', '')
    formatted_item['product_description'] = item['product_description'].replace('\n', '<br />').replace('\t', '')
    formatted_item['images'] = []
    for image_url in item['images']:
        try:
            parts = image_url.split('/')
            img_name = parts.pop()
            name_parts = img_name.split('.')
            img_name = '.'.join([name_parts.pop(0), name_parts.pop()])
            parts.append(img_name)
            formatted_item['images'].append('/'.join(parts))
        except:
            pass
    pairs = []
    for key, value in item['details'].items():
        key_lower = key.lower()
        if key_lower.find('review') != -1:
            continue

        if key_lower.find('rank') != -1:
            continue

        pairs.append('{}:{}'.format(key.strip(), value.strip('(').strip().encode('utf-8')))
    formatted_item['details'] = ';'.join(pairs)
    formatted_item['star'] = item['star']
    formatted_item['reviews'] = item['reviews']
    formatted_item['rank'] = item['rank']
    formatted_item['categories'] = item['categories']

    return formatted_item


class AmazonUsDemoPipeline(object):
    def process_item(self, item, spider):
        return format_detail(item)


class InvalidSettingsException(Exception):
    pass


class ElasticSearchPipeline(object):
    settings = None
    es = None
    items_buffer = []
    id_key = None
    max_retry = 3

    @classmethod
    def validate_settings(cls, settings):
        def validate_setting(setting_key):
            if settings[setting_key] is None:
                raise InvalidSettingsException('%s is not defined in settings.py' % setting_key)

        required_settings = {'ELASTICSEARCH_INDEX'}

        for required_setting in required_settings:
            validate_setting(required_setting)

    @classmethod
    def init_es_client(cls, crawler_settings):
        es_timeout = crawler_settings.get('ELASTICSEARCH_TIMEOUT', 60)

        es_servers = crawler_settings.get('ELASTICSEARCH_SERVERS', 'localhost:9200')
        es_servers = es_servers if isinstance(es_servers, list) else [es_servers]

        es_settings = dict()
        es_settings['hosts'] = es_servers
        es_settings['timeout'] = es_timeout

        if crawler_settings.get('ELASTICSEARCH_USERNAME') and \
            crawler_settings.get('ELASTICSEARCH_PASSWORD'):
            es_settings['http_auth'] = (
                crawler_settings['ELASTICSEARCH_USERNAME'],
                crawler_settings['ELASTICSEARCH_PASSWORD'])

        es = Elasticsearch(**es_settings)

        return es

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        cls.validate_settings(ext.settings)
        ext.es = cls.init_es_client(crawler.settings)
        ext.max_retry = crawler.settings.get('ELASTICSEARCH_MAX_RETRY', 3)
        ext.id_key = crawler.settings.get('ELASTICSEARCH_ID_KEY')
        return ext

    def index_item(self, item):
        index_name = self.settings['ELASTICSEARCH_INDEX']
        index_action = {
            '_index': index_name,
            '_type': '_doc',
            '_op_type': 'index',
            '_source': dict(item)
        }

        if self.id_key is not None and self.id_key in item:
            index_action['_id'] = item[self.id_key]

        self.items_buffer.append(index_action)

        if len(self.items_buffer) >= self.settings.get('ELASTICSEARCH_BUFFER_LENGTH', 500):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        helpers.bulk(self.es, self.items_buffer)
        retry = self.max_retry
        while retry > 0:
            try:
                helpers.bulk(self.es, self.items_buffer)
                break
            except (ConnectionTimeout, ConnectionError, SSLError, TransportError):
                time.sleep(retry)
                retry -= 1
                continue
            except RequestError as e:
                break
            except Exception as e:
                raise e

    def process_item(self, item, spider):
        if isinstance(item, (types.GeneratorType, list)):
            for each in item:
                self.process_item(each, spider)
        else:
            self.index_item(item)
            logging.debug(
                'Item has been sent to Elastic Search %s',
                self.settings['ELASTICSEARCH_INDEX'])

        return item

    def close_spider(self, spider):
        if len(self.items_buffer):
            self.send_items()

class AmazonUsDetailPipeline(ElasticSearchPipeline):
    def process_item(self, item, spider):
        formatted_item = format_detail(item)
        formatted_item['images'] = ';'.join(formatted_item['images'])
        formatted_item['time'] = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%S')

        if not formatted_item['asin'] or not formatted_item['title']:
            raise DropItem('Missing asin or title')

        super(AmazonUsDetailPipeline, self).process_item(formatted_item, spider)

        return item


class AmazonUsOfferListingPipeline(ElasticSearchPipeline):
    def process_item(self, item, spider):
        offer_listing_item = dict()
        offer_listing_item.update(item)
        offer_listing_item['time'] = datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H:%M:%S')

        if not offer_listing_item['asin']:
            raise DropItem('Missing asin')

        super(AmazonUsOfferListingPipeline, self).process_item(offer_listing_item, spider)

        return item
