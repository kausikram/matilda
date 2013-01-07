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
            link = getattr(settings, "BLOG_LINK", "") + "/" + p["output_file_name"] + ".html"
            item = PyRSS2Gen.RSSItem(
                 title = p["title"],
                 link = link,
                 description = p["content"],
                 guid = PyRSS2Gen.Guid(link),
                 pubDate = p["pub_date"])
            items.append(item)

        rss = PyRSS2Gen.RSS2(
            title = getattr(settings, "BLOG_TITLE", ""),
            link = getattr(settings, "BLOG_LINK", ""),
            description = getattr(settings, "BLOG_DESCRIPTION", ""),
            lastBuildDate = datetime.datetime.now(),
            items = items)

        return rss.to_xml(encoding="utf-8")