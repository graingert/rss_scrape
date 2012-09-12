# Scrapy settings for rss_scrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'rss_scrape'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['rss_scrape.spiders']
NEWSPIDER_MODULE = 'rss_scrape.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

LOG_LEVEL = 'INFO'

DEFAULT_REQUEST_HEADERS = {
    'Accept' : "application/atom+xml,application/rdf+xml,application/rss+xml,application/x-netcdf,text/html,application/xhtml+xml,application/xml;q=0.9,text/xml;q=0.2,*/*;q=0.1",
    'Accept-Language' : 'en',
}

FEED_FORMAT = 'csv'
FEED_URI = './items.csv'
