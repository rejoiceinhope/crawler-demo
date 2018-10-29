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

You can run this demo by:

    AMAZON_CAPTCHA_RESOLVER_USERNAME=<your-deathbycaptcha-username> AMAZON_CAPTCHA_RESOLVER_PASSWORD=<your-deathbycaptcha-password> scrapy crawl -a asins_path=./test_asins.txt -t csv -o <your-detail-path> detail_loader
