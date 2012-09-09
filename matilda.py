import os, codecs
import json

from flask import Flask, render_template, request
import settings

from storages import get_storage
from compose import Composer

app = Flask(__name__)

error_tuple = ("Bad Params",400,{"Content-Type":"text/plain"})

class Matilda(object):
    def __init__(self,*args,**kwargs):
        self.storage = get_storage()
        self.composer = Composer()

    def is_valid_post(self,post_id):
        return self.storage.is_valid_post(post_id)

    def get_post(self, post_id):
        return self.storage.get_post(post_id)

    def get_post_id_from_request_data(self, post_data):
        post_params = json.loads(post_data)
        return post_params.get("post_id", None)

    def get_line_data(self,post):
        if type(post["pub_date"]) != type("abcd"):
            post["pub_date"] = post["pub_date"].strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps(post)

    def edit_post(self, post_data):
        post = json.loads(post_data)
        post["pub_date"] = self.get_post(post["post_id"])["pub_date"]
        return_post =  self.storage.edit_post(post,post["post_id"])
        self.composer.build_all()
        return return_post

    def create_post(self, post_data):
        post = json.loads(post_data)
        return_post =  self.storage.create_post(post)
        self.composer.build_all()
        return return_post


@app.route('/')
def index():
    return render_template("control.html")

@app.route('/post/', methods=['POST', 'GET'])
def get_edit_or_create_post():
    if request.method == "GET":
        post_id = request.args.get("post_id",None)
        m = Matilda()
        if not m.is_valid_post(post_id):
            return error_tuple
        json_data = m.get_line_data(m.get_post(post_id))

    if request.method == "POST":
        m = Matilda()
        post_data = request.form["data"]
        post_id = m.get_post_id_from_request_data(post_data)
        if post_id:
            if m.is_valid_post(post_id):
                post = m.edit_post(post_data)
                json_data = m.get_line_data(post)
            else:
                return error_tuple
        else:
            post = m.create_post(post_data)
            json_data = m.get_line_data(post)

    return (json_data, 200, {"Content-Type":"application/json"})


if __name__ == '__main__':
    app.run(debug=True)