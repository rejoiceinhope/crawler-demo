# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import io

from setuptools import setup, find_packages

def read_file(filename):
    with io.open(filename) as fp:
        return fp.read().strip()

def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='amazon_us_demo',
    version='0.1.0',
    description='Amazon.com detail page and offer listing page crawler demo.',
    long_description=open('README.md').read(),
    keywords='scrapy web-scraping amazon.com product-detail offer-listing',
    license='New BSD License',
    author="Neal Wong",
    author_email='qwang16@olivetuniversity.edu',
    url='https://github.com/hyan15/crawler-demo/tree/redis/amazon_us_demo',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=find_packages(),
    entry_points= {'scrapy': ['settings = %(settings)s']},
    install_requires=read_requirements('requirements.txt')
)
