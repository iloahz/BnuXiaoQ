#-*- encoding: utf-8 -*-

from func import *
import urllib
#from google.appengine.api import memcache
import json
import webapp2

def validate(c):
    if db.GqlQuery('SELECT * FROM Classroom WHERE building = :1', c).get():
        return True
    return False

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    q = db.GqlQuery('SELECT * FROM Classroom WHERE building = :1 ORDER BY name ASC', Content)
    Content = ''
    upd = None
    for c in q.fetch(limit = 999):
        if not upd:
            upd = c.updateTime
        Content += c.name + ': '
        tmp = ''
        for i in range(0, 12):
            if c.schedule[i] == '0':
                tmp += 'O'
            else:
                tmp += 'X'
            if i == 3 or i == 7:
                tmp += ' '
        if tmp.find('O') >= 0:
            Content += tmp + '\n'
    Content += '\n更新时间：'
    Content += (upd + datetime.timedelta(hours = 8)).strftime('%m月%d日 %H:%M')
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def getOrCreateClassroomByName(n):
    c = db.GqlQuery('SELECT * FROM Classroom WHERE name = :1', n).get()
    if not c:
        c = Classroom()
        c.name = n
        c.save()
    return c

class FetchHandler(webapp2.RequestHandler):
    def get(self):
        url = 'http://class.bnubaike.cn/api.ashx'
        res = urlfetch.fetch(url).content
        j = json.loads(res)
        for b in j['buildings']:
            bn = b['name']
            for r in b['rooms']:
                c = getOrCreateClassroomByName(r['n'])
                c.building = bn
                c.seats = int(r['s'])
                c.schedule = r['v']
                c.save()

app = webapp2.WSGIApplication([
    ('/classroom/fetch', FetchHandler)
], debug = True)