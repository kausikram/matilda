import os, sys, codecs, hashlib, time
from datetime import datetime
from bs4 import BeautifulSoup
import json
import settings
from storages import get_storage



def get_item(item_tag):
    item = {}
    item["content"] = item_tag.find("encoded").string
    item["pub_date"] = datetime.strptime(item_tag.find("pubDate").string, "%a, %d %b %Y %H:%M:%S +0000") if item_tag.find("pubDate").string else ""
    item["wp_post_id"] = item_tag.find("post_id").string
    item["title"] = item_tag.find("title").string
    item["post_type"] = item_tag.find("post_type").string
    item["wp_url"] = item_tag.find("link").string
    item["status"] = item_tag.find("status").string
    item["format"] = "html"
    if item_tag.find("meta_key",text="dsq_thread_id"):
        item["dsq_thread_id"] = item_tag.find("meta_key",text="dsq_thread_id").find_next_sibling().string

    return item

def import_wp_data(file_path):
    posts = []
    storage = get_storage()
    with open(os.path.abspath(file_path)) as f:
        bs = BeautifulSoup(f.read(),["xml", "lxml"])
        for index, item_tag in enumerate(bs.findAll("item")):
            post = get_item(item_tag)
            storage.create_post(post)
            print index, post["title"]
            posts.append(post)
    print "post len", len(posts)
    return posts

if __name__ =="__main__":
    import_wp_data(sys.argv[1])
