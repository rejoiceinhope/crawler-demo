scrapy-user-agents
=====================

Random User-Agent middleware picks up ``User-Agent`` strings based on `Python User Agents <https://github.com/selwin/python-user-agents>`__ and `MDN <https://developer.mozilla.org/en-US/docs/Web/HTTP/Browser_detection_using_the_user_agent>`__.

Installation
-------------

The simplest way is to install it via `pip`:

    pip install scrapy-user-agents

Configuration
-------------

Turn off the built-in ``UserAgentMiddleware`` and add
``RandomUserAgentMiddleware``.

In Scrapy >=1.0:

.. code:: python

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    }

In Scrapy <1.0:

.. code:: python

    DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    }

User-Agent File
---------------------------

A default User-Agent file is included in this repository, it contains about 2200 user agent strings collected from <https://developers.whatismybrowser.com/> using <https://github.com/hyan15/crawler-demo/tree/master/crawling-basic/common_user_agents>. You can supply your own User-Agent file by set ``RANDOM_UA_FILE``.


Configuring User-Agent type
---------------------------

There's a configuration parameter ``RANDOM_UA_TYPE`` in format ``<device_type>.<browser_type>``, default is ``desktop.chrome``. For device_type part, only ``desktop``, ``mobile``, ``tablet`` are supported. For browser_type part, only ``chrome``, ``firefox``, ``safari``, ``ie``, ``safari`` are supported. If you don't want to fix to only one browser type, you can use ``random`` to choose from all browser types.

You can set ``RANDOM_UA_SAME_OS_FAMILY`` to True to just use user agents that belong to the same os family, such as windows, mac os, linux, or android, ios, etc. Default value is True.

Usage with `scrapy-proxies`
---------------------------

To use with middlewares of random proxy such as `scrapy-proxies <https://github.com/aivarsk/scrapy-proxies>`_, you need:

1. set ``RANDOM_UA_PER_PROXY`` to True to allow switch per proxy

2. set priority of ``RandomUserAgentMiddleware`` to be greater than ``scrapy-proxies``, so that proxy is set before handle UA


Configuring Fake-UserAgent fallback
-----------------------------------

There's a configuration parameter ``FAKEUSERAGENT_FALLBACK`` defaulting to
``None``. You can set it to a string value, for example ``Mozilla`` or
``Your favorite browser``, this configuration can completely disable any
annoying exception.
