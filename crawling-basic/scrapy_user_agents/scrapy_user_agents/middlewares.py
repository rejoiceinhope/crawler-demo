# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import os
import logging

from scrapy_user_agents.user_agent_picker import UserAgentPicker

logger = logging.getLogger(__name__)

class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        fallback = crawler.settings.get('RANDOM_UA_FALLBACK', None)
        per_proxy = crawler.settings.getbool('RANDOM_UA_PER_PROXY', False)
        ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'desktop.chrome')
        same_os_family = crawler.settings.getbool('RANDOM_UA_SAME_OS_FAMILY', True)
        ua_file = crawler.settings.get('RANDOM_UA_FILE')
        if ua_file is None:
            cur_dir, _ = os.path.split(__file__)
            ua_file = os.path.join(cur_dir, 'default_uas.txt')
        else:
            ua_file = os.path.abspath(os.path.expanduser(ua_file))

        uas = []
        with open(ua_file) as ua_fh:
            for line in ua_fh:
                uas.append(line.strip())
        self.ua_picker = UserAgentPicker(uas, ua_type, same_os_family, per_proxy, fallback)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        proxy = request.meta.get('proxy')
        if proxy:
            logger.debug('Proxy is detected %s', proxy)

        ua = self.ua_picker.get_ua(proxy)
        logger.debug('Assigned User-Agent %s', ua)
        request.headers.setdefault('User-Agent', ua)
