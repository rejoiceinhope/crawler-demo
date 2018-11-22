# -*- coding: utf-8 -*-

# Copyright © 2018 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com


import os
import sys
import argparse
import time

import redis

def parse_args():
    parser = argparse.ArgumentParser(description='Add seeds to crawl.')
    parser.add_argument(
        '-u', '--redis_uri', default='redis://localhost:6379', help='Redis server uri')
    parser.add_argument(
        '-q', '--qps', type=float, default=4, help='Seeds add rate in seconds.')
    parser.add_argument(
        '-k', '--start_urls_key', default='detail_loader:start_urls', help='Start urls key.')
    parser.add_argument('asins_path', help='Asins to process.')

    command_args = parser.parse_args()

    return command_args

args = parse_args()
qps = args.qps
start_urls_key = args.start_urls_key
asins_path = os.path.abspath(os.path.expanduser(args.asins_path))
if not os.path.isfile(asins_path):
    print('Could not find asins path - %s' % args.asins_path)
    sys.exit(1)

r = redis.Redis.from_url(args.redis_uri)
last_send_time = None
try:
    with open(asins_path) as asins_fh:
        for line in asins_fh:
            asin = line.strip()

            if last_send_time:
                wait_time = 1 / qps - (time.time() - last_send_time)
                if wait_time > 0:
                    print("Waiting %.3fs to send next message" % wait_time)
                    time.sleep(wait_time)

            last_send_time = time.time()

            r.lpush(start_urls_key, asin)
            print('Added %s' % asin)
except (KeyboardInterrupt, SystemExit):
    print('Exiting, please wait...')
finally:
    pass
