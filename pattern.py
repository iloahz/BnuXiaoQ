import webapp2
from func import *
from google.appengine.ext.webapp import template
import os

def validate(c):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', c).get()
    if p:
        return True
    return False

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', Content).get()
    Content = p.output
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def createOrUpdatePattern(i, o):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', i).get()
    if not p:
        p = Pattern()
        p.input = i
    p.output = o
    p.save()

class PatternHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template', 'pattern.html')
        self.response.write(template.render(path, {}))
    def post(self):
        i = self.request.get('input')
        o = self.request.get('output')
        createOrUpdatePattern(i, o)
        self.redirect('/pattern')

app = webapp2.WSGIApplication([
    ('/pattern', PatternHandler)
], debug = True)