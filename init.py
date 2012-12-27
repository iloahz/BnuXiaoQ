#-*- encoding: utf-8 -*-

import webapp2
from func import *

class InitHandler(webapp2.RequestHandler):
    def get(self):
        if not getTopTen():
            for i in range(0, 10):
                t = TopTenTopic()
                t.url = ''
                t.title = ''
                t.authorPic = ''
                t.rank = i
                t.save()
        p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', u'喵').get()
        if not p:
            p = Pattern()
            p.input = u'喵'
            p.output = u'不要学人家啦，喵~'
            p.save()

app = webapp2.WSGIApplication([
    ('/init', InitHandler)
], debug = True)