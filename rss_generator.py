import datetime
import PyRSS2Gen
import settings

class RssGenerator(object):
    def __init__(self):
        pass

    def generate(self,posts):
        print posts
        items = []
        for p in posts:
            item = PyRSS2Gen.RSSItem(
                 title = p["title"],
                 link = "http://www.dalkescientific.com/news/030906-PyRSS2Gen.html",
                 description = p["content"],
                 guid = PyRSS2Gen.Guid("http://www.dalkescientific.com/news/030906-PyRSS2Gen.html"),
                 pubDate = p["pub_date"])
            items.append(item)

        rss = PyRSS2Gen.RSS2(
            title = getattr(settings, "BLOG_TITLE", ""),
            link = getattr(settings, "BLOG_LINK", ""),
            description = getattr(settings, "BLOG_DESCRIPTION", ""),
            lastBuildDate = datetime.datetime.now(),
            items = items)

        return rss.to_xml(encoding="utf-8")