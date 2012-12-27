#-*- encoding: utf-8 -*-

import os
import webapp2
from google.appengine.ext.webapp import template
from func import *
import topten
import library
import pattern
import weather

def defaultAnswer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = '''小Q都听不懂你在说什么诶...坏人!
输入“h”查看帮助试试
顺便说一句，输入都不带引号哦~~'''
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def saveMsgLog(fromUser, req):
    u = getOrCreateUserById(fromUser)
    u.msgCount += 1
    u.save()
    m = MessageLog()
    m.fromUser = u
    m.req = unicode(req)
#    m.res = res
    m.save()

def normalizeContent(c):
    c = c.lower().strip()
    a = db.GqlQuery('SELECT * FROM Alias WHERE origin = :1', c).get()
    if a:
        c = a.result
    return c

def createOrUpdateAlias(o, r):
    a = db.GqlQuery('SELECT * FROM Alias WHERE origin = :1', o).get()
    if not a:
        a = Alias()
        a.origin = o
    a.result = r
    a.save()

class AliasHandler(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'template', 'alias.html')
        self.response.write(template.render(path, {}))
    def post(self):
        o = self.request.get('origin')
        r = self.request.get('result')
        createOrUpdateAlias(o, r)
        self.redirect('/alias')

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        s = self.request.GET['signature']
        t = self.request.GET['timestamp']
        n = self.request.GET['nonce']
        e = self.request.GET['echostr']
        if validateSource(timestamp = t, nonce = n, signature = s):
            self.response.write(e)
        else:
            self.response.write('Bad boy!')
    def post(self):
        x = self.request.body
        ToUserName, FromUserName, CreateTime, MsgType, Content = parseTextXml(x)
        ToUserName, FromUserName = FromUserName, ToUserName
        Content = normalizeContent(Content)
        logging.info('Received message "{}" from "{}"'.format(Content, ToUserName))
        if pattern.validate(Content):
            res = pattern.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        elif topten.validate(Content):
            res = topten.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        elif library.validate(Content):
            res = library.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        elif weather.validate(Content):
            res = weather.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        else:
            res = defaultAnswer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        saveMsgLog(ToUserName, Content)
        self.response.write(res)

app = webapp2.WSGIApplication([
    ('/', IndexHandler),
    ('/alias', AliasHandler)
], debug = True)