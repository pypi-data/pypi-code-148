import feedparser
from ..base import *

class RSSFeed(object):
    def get_feed(self, url: str) -> List[RSS_Schema]:
        d = feedparser.parse(url)
        rss = []
        for k in d['entries']:
            post = {}
            for k, v in k.items():
                post[k] = v
                post['rss_url'] = url
            rss.append(RSS_Schema(**post))
        return rss
