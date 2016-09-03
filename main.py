#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import string
#from string import maketrans

template_dir=os.path.join(os.path.dirname(__file__), 'template')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

form="""
<form action='/testform' method=post>
<input name="q">
<input type=submit name=submit value=submit>
</form>
"""
class Handler (webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(**kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        return

# print fizzbuzz up to n (n/3=0 ->fizz, n/5=0 ->buzz, n/{3 and 5}=0-->FizzBuzz)
class FBHandler(Handler):
    def get(self):
        n = self.request.get('n',0)
        n = n and int(n)
        self.render('fizzbuzz.html', n=n)

class MainPage(Handler):
    def get(self):
        items = self.request.get_all('food')
        self.render('shoping_list.html', items=items)
        
class ROT13Handler(Handler):
    def rot13(self, s):
        t13 = string.maketrans( 
            "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
            "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
        return s.encode('utf-8').translate(t13)
        
    def get(self):
        itext1 = self.request.get('text')
        itext = itext1
        if itext:
            itext = self.rot13(itext1)
        self.render('rot13.html', itext=itext)

    def post(self):
        itext1 = self.request.get('text')
        itext = itext1
        if itext:
            itext = self.rot13(itext1)
        self.render('rot13.html', itext=itext)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type']='text/html'
        self.response.write(form)

class TestHandler(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type']='text/plain'
        q = self.request.get("q");
        self.response.write(self.request)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', TestHandler),
    ('/fizzbuzz', FBHandler),
    ('/rot13', ROT13Handler),
], debug=True)
