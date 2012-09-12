# This is a spider that can crawl RSS feeds in a version independent manner. it uses Mark pilgrim's excellent feedparser utility to parse RSS feeds. You can read about the nightmares of  RSS incompatibility [here](http://diveintomark.org/archives/2004/02/04/incompatible-rss) and  download feedparser that strives to resolve it from [here](http://feedparser.org/docs/)
# The scripts processes only certain elements in the feeds(title, link and summary)
# The items may be saved in the Item pipeline which I leave to you. 
# 
# Please let me know about any discrepencies you may find in the technical and functional aspects of this scipt.
# 
# -Sid

from scrapy.spider import BaseSpider

from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
from scrapy.http import Request
import feedparser
import re
from urlparse import urlparse
import xml.sax

import lxml.html
from lxml.etree import ParserError
from lxml.cssselect import CSSSelector
from scrapy import log

from rss_scrape.items import RssFeedItem, RssEntryItem
import chardet
import datetime
from dateutil.tz import tzutc

class RSSSpider(BaseSpider):
    name = "rss_scrape"
    _allowed_domain = {"soton.ac.uk", "southampton.ac.uk"}
    start_urls = [
        "http://blog.soton.ac.uk/",
        "http://blog.soton.ac.uk/data/",
        "http://www.soton.ac.uk/sitemap.html",
    ]
    _gathered_fields = ('published_parsed' ,'title' ,  'link' ,'summary');
    
    def parse(self, response):
        try:
            document = lxml.html.fromstring(response.body)
            document.make_links_absolute(base_url=response.url, resolve_base_href=True)
        except ParserError:
            #Document is probably empty, return no items
            return
        
        rss_elements = CSSSelector('rss, feed, xml, rdf')(document)
        character_set = chardet.detect(response.body)["encoding"]
        # is this an rss file
        if all((rss_elements, character_set)):
            try:
                feed = feedparser.parse(
                    url_file_stream_or_string = response.body,
                    #request_headers = response.request.headers,
                    #response_headers = response.headers
                )
                
                #seeing as we've requested the document, might as well save it
                if feed.version:
                    rssFeedItem = RssFeedItem(url = response.url);
                    
                    for key in {'title', 'summary', 'link'} & feed.feed.__dict__.viewkeys():
                        rssFeedItem[key] = getattr(parsed_feed.feed, key)
                                        
                    rssFeedItem['entries'] = []
                    
                    for entry in feed.entries:
                        entry_item = RssEntryItem()
                        
                        published = entry.get("published_parsed", None)
                        if published:
                            entry["published"] = datetime.datetime(*(published[0:6]), tzinfo=tzutc()).isoformat()
                        
                        for key in {'title', 'link', 'summery', 'published'} & entry.viewkeys():
                            entry_item[key] = entry[key]
                        
                        rssFeedItem['entries'].append(entry_item);
                    yield rssFeedItem
                else:
                    self.log("{url} looked like a feed, but wasn't one".format(url=response.url), level=log.DEBUG)
            except xml.sax.SAXException:
                pass
        urls = set(
            map(
                lambda x: x[2], #the link is third element from items in iterlinks
                document.iterlinks()
            )
        )
        for url in urls:
            if urlparse(url).netloc.endswith(tuple(self._allowed_domain)):
                yield Request(url)
   
class MalformedURLException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
