#-*- encoding: utf-8 -*-

import webapp2
from func import *
import hello
import topten
import help
import library

def defaultAnswer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = '小Q都听不懂你在说什么诶...坏人!'
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def saveMsgLog(fromUser, req, res):
    u = getOrCreateUserById(fromUser)
    u.msgCount += 1
    u.save()
    m = MessageLog()
    m.fromUser = u
    m.req = req
    m.res = res
    m.save()

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
        Content = Content.lower()
        logging.info('Received message "{}" from "{}"'.format(Content, FromUserName))
        if hello.validate(Content):
            res = hello.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        elif help.validate(Content):
            res = help.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        elif topten.validate(Content):
            res = topten.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        elif library.validate(Content):
            res = library.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        else:
            res = defaultAnswer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        saveMsgLog(FromUserName, x, res)
        self.response.write(res)

app = webapp2.WSGIApplication([
    ('/', IndexHandler)
], debug = True)