import os
import webapp2
import jinja2
import hashlib
import hmac
from string import letters
from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__), 'template')
jinja_env=jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
#
SECRET='t0p5ecret'
def hash_str(s):
    #return hashlib.md5(s).hexdigest();
    return hmac.new(SECRET, s).hexdigest();

# -----------------
# User Instructions
# 
# Implement the function make_secure_val, which takes a string and returns a 
# string of the format: 
# s,HASH
def make_secure_val(s):
    #return s+"|"+hash_str(s);
    return '%s|%s' %(s, hash_str(s))
# -----------------
# User Instructions
# 
# Implement the function check_secure_val, which takes a string of the format 
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None 

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val) :
        return int(val)
    else :
        return 0
        
# Base handler
class Handler (webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(**kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        return

class MainPage(Handler):
    def get(self):
        self.response.headers['Content-Type']='text/plain'
        visits = 0
        visit_cookie_str = self.request.cookies.get('visits')
        if visit_cookie_str:
            visits = check_secure_val(visit_cookie_str)
        visits += 1
        nc = make_secure_val(str(visits))
        self.response.headers.add_header('Set-Cookie', 'visits=%s' %nc)
        self.write('\nCookie Received: %s' %visit_cookie_str)
        self.write('\nYour visit count: %d' %visits)
        self.write('\nYour Set-Cookie: %s' %nc)
        

app = webapp2.WSGIApplication([
        ('/', MainPage),
        ], debug=True)
        
        