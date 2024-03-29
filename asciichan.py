import os
import webapp2
import jinja2
#import google
from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__), 'template')
jinja_env=jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

class Handler (webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(**kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        return

class AsciiArt(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

        
class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        #arts=[AsciiArt(title='t1', art='body')]
        # This should return cursor
        arts = db.GqlQuery("select * from AsciiArt order by created desc")
        #arts = Art.gql("select * from art order by created desc")
        self.render('front.html', title=title, art=art, error=error, arts=arts)
        return
        
    def get(self):
        self.render_front()
        return
        
    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')
        error=""
        if title and art :
            a = AsciiArt(title=title, art=art)
            a.put()
            self.redirect('/')
        else :
            error="we need title and art"
            self.render_front(title, art, error)
        return

app = webapp2.WSGIApplication([
        ('/', MainPage),
        ],debug=True)        
        