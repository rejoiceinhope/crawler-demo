# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

from setuptools import setup

setup(
    name='scrapy_user_agents',
    version='0.1.1',
    description='Automatically pick an User-Agent for every request',
    long_description=open('README.rst').read(),
    keywords='scrapy proxy user-agent web-scraping',
    license='New BSD License',
    author="Neal Wong",
    author_email='ibprnd@gmail.com',
    url='https://github.com/hyan15/crawler-demo/tree/master/crawling-basic/scrapy_user_agents',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=[
        'scrapy_user_agents',
    ],
    package_dir={'scrapy_user_agents': 'scrapy_user_agents'},
    package_data={'scrapy_user_agents': ['default_uas.txt']},
    install_requires=[
        'user-agents'
    ],
)
