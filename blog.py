import os
import webapp2
import jinja2
from string import letters
#import google
from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__), 'template')
jinja_env=jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

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
# GQL storage
def blog_key(name='default'):
    return db.Key.from_path('blogs', name)
    
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
#    last_modified=db.DateTimeProperty(auto_now = True)
#    def render(self):
#        self.render_text=self.content.replace('\n', '<br>')
#        return render_str("blog.html", p=self)


class NewPostPage(Handler):
    def render_newpost(self, subject="", content=""):
        error=""
        if subject=="" and content != "":
            error = "Subjec can't be empty"
        elif subject!="" and content == "":
            error = "Content can't be empty"
        
        self.render('newpost.html', subject=subject, content=content, error=error)
        return
        
    def get(self):    
        self.render_newpost()
        return
    
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        if subject!="" and content != "" :
            blog = Blog(subject=subject, content=content)
            blog.put()
            blog_id=str(blog.key().id())
            self.redirect('/blog/'+blog_id)
        else :
            self.render_newpost(subject, content)
        return

        
class BlogPage(Handler):
    def get(self):
        #blog=[Blog(subject='blog1', content='blog content')]
        # This should return cursor
        blogs = db.GqlQuery("select * from Blog order by created desc")
        #blogs = Blog.all().order('-created')
        self.render('blog.html', blogs=blogs)
        return

# Render a single post
class BlogPageId(Handler):
    def get(self, id):        
        #blogs = db.GqlQuery("select * from Blog where id=" + id)
        blog = Blog.get_by_id(int(id))
        self.render("blog.html", blogs=[blog])

app = webapp2.WSGIApplication([
        ('/blog', BlogPage),
        ('/blog/newpost', NewPostPage),
        ('/blog/(\d+)', BlogPageId),
        ], debug=True)
        
        