common_user_agents
=====================

Collect common used browser user agent strings from <https://developers.whatismybrowser.com/>.
Current supported browsers are chrome, internet explorer, safari, firefox, you can extend to more browsers on your own.

Installation
-------------

The simplest way is to install it via `pip`:

    pip install -r requirements.txt

Execute:
-------------

The following command will write out user agent strings to uas.txt in csv format:

    scrapy crawl -t csv -o uas.txt whatismybrowser

You can use `-a` to pass "max_page" argument to control how many pages to crawl, by default max_page is 10.