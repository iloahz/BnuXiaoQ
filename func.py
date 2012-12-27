import logging
import hashlib
from xml.dom import minidom
from model import *
import time, datetime
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def validateSource(timestamp, nonce, signature):
    logging.info('checking timestamp = "{}", nonce = "{}", signature = "{}"'.format(timestamp, nonce, signature))
    token = '1463892301'
    l = [token, timestamp, nonce]
    l.sort()
    s = ''.join(l)
    s = hashlib.sha1(s).hexdigest()
    return s == signature

def parseTextXml(x):
    d = minidom.parseString(x)
    ToUserName = d.getElementsByTagName('ToUserName')[0].childNodes[0].data
    FromUserName = d.getElementsByTagName('FromUserName')[0].childNodes[0].data
    CreateTime = d.getElementsByTagName('CreateTime')[0].childNodes[0].data
    MsgType = d.getElementsByTagName('MsgType')[0].childNodes[0].data
    Content = d.getElementsByTagName('Content')[0].childNodes[0].data
    return ToUserName, FromUserName, CreateTime, MsgType, Content

def genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content, FuncFlag = '0'):
    r = minidom.getDOMImplementation()
    d = r.createDocument(None, 'xml', None)
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
    t = d.createCDATASection(CreateTime)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('MsgType')
    t = d.createCDATASection(MsgType)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('Content')
    t = d.createCDATASection(Content)
    s.appendChild(t)
    x.appendChild(s)
    s = d.createElement('FuncFlag')
    t = d.createTextNode(FuncFlag)
    s.appendChild(t)
    x.appendChild(s)
    return x.toxml()

def getTopTen():
    t = TopTenTopic.all().fetch(limit = 10)
    return t

def getOrCreateUserById(id):
    u = db.GqlQuery('SELECT * FROM User WHERE wechatId = :1', id).get()
    if not u:
        u = User(wechatId = id)
        u.save()
    return u