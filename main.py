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
import re
#from string import maketrans

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

template_dir=os.path.join(os.path.dirname(__file__), 'template')
#jinja_env=jinja2.Environment(
#  loader=jinja2.FileSystemLoader(template_dir))
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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

class LoginHandler(Handler):
    def validate_u(self, uname):        
        ru = USER_RE.match(uname)
        if ru == None:
            return "Invalid username"
        return ""        
    
    def validate_p(self, p1, p2):
        if p1=="" or p2=="":
            return "Enter a valid password"
            
        if p1 != p2:
            return "Password mismatch";
            
        rp1 = PASS_RE.match(p1);
        rp2 = PASS_RE.match(p2);            
        if rp1 == None or rp2 == None:
            return "Password invalid"        
        
        return ""
    
    def validate_e(self, email):
        err = ""
        if (email != ""):
            re = EMAIL_RE.match(email)
            if re == None:
                err="Invalid email"        
        return err
        
    def get(self):
        self.render('login.html')

    def post(self):
        # Username
        username = self.request.get('username')
        eusername = self.validate_u(username)            
        # Password
        password = self.request.get('password')
        verify = self.request.get('verify')
        epassword = self.validate_p(password, verify)
        # Email optional
        email = self.request.get('email')
        eemail = self.validate_e(email)
        if eusername == "" and eemail == "" and epassword == "":
            self.redirect('/welcome?username='+username);            
            # items = {
                # 'username': username,
                # 'email': email
            # }
            # wt = jinja_env.get_template('welcome.html')
            # html_text = wt.render(items)
            # self.write(html_text)
        else:
            values = {
                'username' : username,
                'eusername' : eusername,
                'epassword' : epassword,
                'email' : email,
                'eemail' : eemail
            }        
            logt = jinja_env.get_template('login.html')
            html_login = logt.render(values)
            self.write(html_login)

class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        values = {
                'username' : username,
                }
        welt = jinja_env.get_template('welcome.html')
        html_welcome = welt.render(values)
        self.write(html_welcome)                

        
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/testform', TestHandler),
    ('/fizzbuzz', FBHandler),
    ('/rot13', ROT13Handler),
    ('/login', LoginHandler),
    ('/welcome', WelcomeHandler),
], debug=True)
