# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class RssItem(Item):
    title = Field()# the Title of the feed
    link = Field()# the URL to the web site(not the feed)
    summary = Field();# short description of feed

class RssFeedItem(RssItem):
    entries = Field();# will contain the RSSEntrItems
    url = Field()# the URL to the feed(not the web site)

class RssEntryItem(RssItem):
    published = Field()
