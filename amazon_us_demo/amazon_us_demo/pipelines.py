# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazonUsDemoPipeline(object):
    def process_item(self, item, spider):
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
            except Exception as e:
                spider.logger.exception(e)
                pass
        pairs = []
        for key, value in item['details'].items():
            key_lower = key.lower()
            if key_lower.find('review') != -1:
                continue

            if key_lower.find('rank') != -1:
                continue

            pairs.append('{}:{}'.format(key.strip(), value.strip('(').strip()))
        formatted_item['details'] = ';'.join(pairs)
        formatted_item['star'] = item['star']
        formatted_item['reviews'] = item['reviews']
        formatted_item['rank'] = item['rank']
        formatted_item['categories'] = item['categories']

        return formatted_item
