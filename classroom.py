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
    r = minidom.getDOMImplementation()
    d = r.createDocument(None, 'xml', None)
    #x is the root node
    x = d.createElement('xml')
    s = d.createElement('ToUserName')
    t = d.createCDATASection(ToUserName)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('FromUserName')
    t = d.createCDATASection(FromUserName)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('CreateTime')
    t = d.createTextNode(CreateTime)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('MsgType')
    t = d.createCDATASection('Text')
    s.appendChild(t)
    x.appendChild(s)
    q = db.GqlQuery('SELECT * FROM Classroom WHERE building = :1 ORDER BY name ASC', Content)
    Content = ''
    for c in q.fetch(limit = 999):
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
    s = d.createElement('Content')
    t = d.createCDATASection(Content)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('FuncFlag')
    t = d.createTextNode('0')
    s.appendChild(t)
    x.appendChild(s)
    dat = x.toxml()
    return dat

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