# -*- coding: utf-8 -*-

# Scrapy settings for amazon_us_demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import os

BOT_NAME = 'amazon_us_demo'

SPIDER_MODULES = ['amazon_us_demo.spiders']
NEWSPIDER_MODULE = 'amazon_us_demo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'amazon_us_demo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 360

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.33
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 3

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en-US',
   'Referer': 'https://www.amazon.com'
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'amazon_us_demo.middlewares.AmazonUsDemoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 410,
    'amazon_us_demo.middlewares.AmazonUsCaptchaResolverMiddleware': 450,
    'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'amazon_us_demo.pipelines.AmazonUsDemoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 3
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# RetryMiddleware settings
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 503, 408, 400]

# User agent settings
RANDOM_UA_TYPE = 'desktop.random'
RANDOM_UA_FALLBACK = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
RANDOM_UA_SAME_OS_FAMILY = True


# Amazon captcha resolver settings
AMAZON_CAPTCHA_RESOLVER_ENABLED = True
AMAZON_CAPTCHA_RESOLVER_USERNAME = os.getenv('AMAZON_CAPTCHA_RESOLVER_USERNAME', '')
AMAZON_CAPTCHA_RESOLVER_PASSWORD = os.getenv('AMAZON_CAPTCHA_RESOLVER_PASSWORD', '')
AMAZON_CAPTCHA_RESOLVER_THRESHOLD = os.getenv('AMAZON_CAPTCHA_RESOLVER_THRESHOLD', 32)

PROXY_POOL_ENABLED = True
PROXY_POOL_FILTER_ANONYMOUS = True
PROXY_POOL_FILTER_TYPES = 'https'
PROXY_POOL_FILTER_CODE = 'us'
PROXY_POOL_REFRESH_INTERVAL = 900
PROXY_POOL_CLOSE_SPIDER = False
PROXY_POOL_BAN_POLICY = 'amazon_us_demo.utils.AmazonBanDetectionPolicy'

# CSV Exporter settings
# FIELDS_TO_EXPORT = [
#   'asin', 'rank', 'star', 'reviews', 'categories', 'images', 'author',
#   'title', 'details', 'feature_bullets', 'book_description', 'product_description']

FEED_EXPORTERS = {
    'csv': 'amazon_us_demo.exporters.CustomCsvItemExporter'
}