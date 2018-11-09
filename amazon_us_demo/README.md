amazon_us_demo
=====================

A demo illustrates crawl www.amazon.com detail page with scrapy. Currently supported fields are:
* asin - Amazon ASIN
* rank - Sales Rank in top browse node
* star - Average star of custom reviews
* reviews - Custom Reviews count
* categories - Browse nodes tree
* images - Multiple images are concated by ';'
* author - Multiple authors are concated by ','
* title - Title
* details - Details are key, value pairs. Detail item is concated by ':' and items by ';'
* feature_bullets - Feature bullets are concated by '#FeatureBullets#'
* book_description - book description
* product_description - product description

All line feed characters are replaced by '<pre><br /></pre>'.


Installation
-------------

The simplest way is to install it via `pip`:

    pip install -r requirements.txt


Configuration
-------------

Please refer to amazon_us_demo/settings.py.


Execution
-------------

Before run this demo, the following environment variables should be defined:
* AMAZON_CAPTCHA_RESOLVER_USERNAME - Your deathbycaptcha username
* AMAZON_CAPTCHA_RESOLVER_PASSWORD - Your deathbycaptcha password
* AMAZON_CAPTCHA_RESOLVER_THRESHOLD - Captcha resolve rate threshold, default is 32/s.
* ELASTICSEARCH_SERVERS - Elasticsearch server, default is '127.0.0.1'.
* ELASTICSEARCH_INDEX - Elasticsearch index.
* ELASTICSEARCH_USERNAME - Elasticsearch username.
* ELASTICSEARCH_PASSWORD - Elasticsearch password.
* ELASTICSEARCH_ID_KEY - Elasticsearch index id field name, default is 'asin'.
* ELASTICSEARCH_TIMEOUT - Elasticsearch timeout, default is 60.
* ELASTICSEARCH_MAX_RETRY - Elasticsearch index max retry times, default is 3.
* ELASTICSEARCH_BUFFER_LENGTH - Item count per index operation, default is 500.

You can run this demo by:

    scrapy crawl -a asins_path=./test_asins.txt detail_loader
    scrapy crawl -a asins_path=./test_asins.txt offer_listing_loader
