#-*- encoding: utf-8 -*-

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
    g = db.GqlQuery('SELECT * FROM Global').get()
    i = random.randint(0, g.totalPattern - 2)
    p = db.GqlQuery('SELECT * FROM Pattern')
    for i in p.fetch(limit = 9, offset = i):
        return i.input
    return None

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', Content).get()
    Content = p.output
#    if p.hintNext:
#        Content += '\n\n你也可以再试试“' + p.hintNext + '”哦~'
#    p.hintNext = getRandomPattern()
#    if p.hintNext == p.input:
#        p.hintNext = None
#    p.save()
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def createOrUpdatePattern(i, o):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', i).get()
    if not p:
        p = Pattern()
        p.input = i.lower()
        p.hintNext = getRandomPattern()
        g = db.GqlQuery('SELECT * FROM Global').get()
        g.totalPattern += 1
        g.save()
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