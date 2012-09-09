import time
from datetime import datetime, timedelta
import os, codecs, json
import settings

class FileSystemStorage(object):
    def _make_post_id(self, post):
        t = post["pub_date"]
        filename = str(int(time.mktime(t.timetuple())))
        if self.is_valid_post(filename):
            post["pub_date"] = post["pub_date"] + timedelta((1.0/(24*60*60)))
            return self._make_post_id(post)
        return filename

    def _pre_process(self,raw_data):
        post = json.loads(raw_data)
        if post["pub_date"]:
            post["pub_date"] = datetime.strptime(post["pub_date"], "%Y-%m-%d %H:%M:%S")
        return post

    def _save_post(self, post, post_id):
        post["pub_date"] = post["pub_date"].strftime("%Y-%m-%d %H:%M:%S")
        jsoned_post = json.dumps(post)
        filename = os.path.join(os.path.abspath(settings.POSTS_DIR),post_id+".json")
        f = codecs.open(filename,"w", encoding="utf-8")
        f.write(jsoned_post)
        f.close()

    def clear_storage(self):
        folder = os.path.abspath(settings.OUTPUT_DIR)
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e

    def is_valid_post(self, post_id):
        return os.path.exists(os.path.join(os.path.abspath(settings.POSTS_DIR),post_id+".json"))

    def get_all_posts_by_type(self,status=None,post_type=None):
        post_list = []
        for f_path in os.listdir(os.path.abspath(settings.POSTS_DIR)):
            with open(os.path.join(os.path.abspath(settings.POSTS_DIR),f_path)) as f:
                raw_data = f.read()
            post = self._pre_process(raw_data)
            if status and post["status"] != status:
                continue
            if post_type and post["post_type"] != post_type:
                continue
            post_list.append(post)
        post_list.sort(key=lambda x: x["pub_date"])
        return post_list


    def get_post(self, post_id):
        with open(os.path.join(os.path.abspath(settings.POSTS_DIR),post_id+".json")) as f:
            raw_data = f.read()
        post = self._pre_process(raw_data)
        return post

    def edit_post(self, post, post_id):
        self._save_post(post, post_id)
        return post

    def create_post(self,post):
        post["pub_date"] = datetime.now()
        post_id = self._make_post_id(post)
        post["dsq_thread_id"] = post_id
        self._save_post(post, post_id)
        return post

    def delete_post():
        pass