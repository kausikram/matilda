import codecs, os
import markdown
from jinja2 import Environment, FileSystemLoader
import settings
import re
from storages import get_storage

from unicodedata import normalize

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

class PostOrganizer(object):
    def __init__(self,post_list):
        self.post_list = post_list

    def get_next_link(self,post):
        index = self.post_list.index(post)
        index+=1
        if index < len(self.post_list):
            return self.post_list[index]
        return None

    def get_prev_link(self,post):
        index = self.post_list.index(post)
        index-=1
        if index > 0:
            return self.post_list[index]
        return None

class Composer(object):
    def __init__(self,*args,**kwargs):
        self.post_list = []
        self.post_name_list = []
        loader = FileSystemLoader(os.path.abspath(settings.TEMPLATE_DIR))
        self.env = Environment(loader=loader)
        self.env.globals["settings"] = settings

    def get_output_file_name(self,post, filename):
        if filename in self.post_name_list:
            self.get_output_file_name(post, filename+"_1")
        else:
            post["output_file_name"] = filename

    def build_index_page(self, post):
        self.build_post(post,"index")

    def build_post(self,post, post_name=None):
        template = self.env.get_template('post_page.html')
        if post["format"]=="markdown":
            post["content"] = markdown.markdown(post["content"])
        rendered_template =  template.render({"post":post})
        if not post_name:
            post_name = post["output_file_name"]
        f = codecs.open(os.path.join(os.path.abspath(settings.OUTPUT_DIR), post_name+".html"),"w", encoding="utf-8")
        f.write(rendered_template)
        f.close()

    def is_new_post(self, post):
        return self.post_list.index(post) == len(self.post_list) - 1

    def build(self, post):
        if self.is_new_post(post):
            self.build_index_page(post)
        self.build_post(post, post["output_file_name"])


    def build_all(self):
        storage = get_storage()
        storage.clear_storage()
        self.post_list = storage.get_all_posts_by_type(status="publish")
        for post in self.post_list:
            base_slug_title = slugify(post["title"],"_") if post["title"] else slugify(post["content"][:24],"_")
            self.get_output_file_name(post,base_slug_title)
            self.post_name_list.append(post["output_file_name"])

        self.env.globals["post_manager"] = PostOrganizer(self.post_list)
        for p in self.post_list:
            print p["pub_date"], p["output_file_name"]
            self.build(p)

        print "-" * 50
        print "len of posts", len(self.post_list)
        print "len of post names", len(self.post_name_list)


if __name__=="__main__":
    c = Composer()
    c.build_all()
