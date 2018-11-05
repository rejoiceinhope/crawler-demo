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

## Testing

chef exec rspec
kitchen test