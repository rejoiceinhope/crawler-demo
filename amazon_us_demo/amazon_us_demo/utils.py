# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

from scrapy_proxy_pool.policy import BanDetectionPolicy

def is_robot_check(response):
    return response.xpath('//*[@id="captchacharacters"]').extract_first() is not None


class AmazonBanDetectionPolicy(BanDetectionPolicy):
    def response_is_ban(self, request, response):
        base_ban = super(AmazonBanDetectionPolicy, self).response_is_ban(request, response)
        amazon_ban = is_robot_check(response)

        return base_ban or amazon_ban
