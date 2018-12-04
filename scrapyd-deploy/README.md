# Scrapyd Deploy

This chef cookbook is used to deploy scrapyd as a systemd service.

## Requirements

### Chef

Tested on 13.6.4, but version newer than 12.1 should work just fine. File an [issue](https://github.com/hyan15/crawler-demo/issues) if this isn't the case.

### Platform

The following platforms have been tested with this cookbook:

* ubuntu (16.04) 

## Recipes

### default

Install python, upgrade pip, install scrapyd and setup scrapyd systemd service.

## Attributes

### scrapyd.packages

Pip packages that scrapy projects depend on.

The default is `['Scrapy', 'scrapy-user-agents', 'deathbycaptcha', 'elasticsearch', 'scrapy-redis', 'scrapy_proxy_pool', 'python-dotenv']`

### scrapyd.user

The user used to run scrapyd service.

The default is `"scrapy"`

### scrapyd.group

The group used to run scrapyd service.

The default is `"scrapy"`

### scrapyd.bind_address

Scrapyd web service binding address.

The default is `"0.0.0.0"`

### scrapyd.http_port

Scrapyd web service binding port.

The default is `"6800"`

### scrapyd.max_proc

The maximum number of concurrent Scrapy process that will be started. If unset or 0 it will use the number of cpus available in the system multiplied by the value in max_proc_per_cpu option. Defaults to 0.

### scrapyd.max_proc_per_cpu

The maximum number of concurrent Scrapy process that will be started per cpu. Defaults to 4.

### scrapyd.debug

Whether debug mode is enabled. Defaults to off. When debug mode is enabled the full Python traceback will be returned (as plain text responses) when there is an error processing a JSON API call.

### scrapyd.eggs_dir

The directory where the project eggs will be stored.

The default is `"/var/lib/scrapyd/eggs"`

### scrapyd.dbs_dir

The directory where the project databases will be stored (this includes the spider queues).

The default is `"/var/lib/scrapyd/dbs"`

### scrapyd.logs_dir

The directory where the Scrapy logs will be stored. If you want to disable storing logs set this option empty.

The default is `"/var/log/scrapyd"`

### scrapyd.items_dir

The directory where the Scrapy items will be stored. This option is disabled by default because you are expected to use a database or a feed exporter. Setting it to non-empty results in storing scraped item feeds to the specified directory by overriding the scrapy setting FEED_URI.

The default is `"/var/lib/scrapyd/items"`

### scrapyd.jobs_to_keep

The number of finished jobs to keep per spider. Defaults to 5. This refers to logs and items.

### scrapyd.finished_to_keep

The number of finished processes to keep in the launcher. Defaults to 100. This only reflects on the website /jobs endpoint and relevant json webservices.

### scrapyd.poll_interval

The interval used to poll queues, in seconds. Defaults to 5.0. Can be a float, such as 0.2

### scrapyd.runner

The module that will be used for launching sub-processes. You can customize the Scrapy processes launched from Scrapyd by using your own module.

The default is `"scrapyd.runner"`

### scrapyd.application

A function that returns the (Twisted) Application object to use. This can be used if you want to extend Scrapyd by adding and removing your own components and services.

The default is `"scrapyd.app.application"`

### scrapyd.webroot

A twisted web resource that represents the interface to scrapyd. Scrapyd includes an interface with a website to provide simple monitoring and access to the application’s webresources. This setting must provide the root class of the twisted web resource.

The default is `"scrapyd.website.Root"`

## Testing

chef exec rspec
kitchen test