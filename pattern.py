import webapp2
from func import *
from google.appengine.ext.webapp import template
import os
import random
def validate(c):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', c).get()
    if p:
        return True
    return False

def getRandomPattern():
    if random.randint(0, 1) == 0:
        return
    g = db.GqlQuery('SELECT * FROM Global').get()
    i = random.randint(0, g.totalPattern - 1)
    p = db.GqlQuery('SELECT * FROM Pattern').fetch(limit = 1, offset = i)
    return p.input

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', Content).get()
    Content = p.output
    if p.hintNext:
        Content += '\n你可以再试试“' + p.hintNext + '”哦~\n'
    p.hintNext = getRandomPattern()
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def createOrUpdatePattern(i, o):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', i).get()
    if not p:
        p = Pattern()
        p.input = i.lower()
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