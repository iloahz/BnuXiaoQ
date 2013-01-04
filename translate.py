#-*- encoding: utf-8 -*-

from func import *
import urllib
from google.appengine.api import memcache
import json

def validate(c):
    if c.startswith('d ') or c.startswith('fy '):
        return True
    return False

def answerYoudao(ToUserName, FromUserName, CreateTime, MsgType, Content):
    keyword = ' '.join(Content.split()[1:])
    Content = memcache.get(key = keyword, namespace = 'dict')
    if not Content:
        #get data from youdao
        url = 'http://fanyi.youdao.com/openapi.do?'
        arg = {
            'keyfrom' : 'BnuXiaoQ',
            'key' : '1336627529',
            'type' : 'data',
            'doctype' : 'json',
            'version' : '1.1',
            'q' : keyword
        }
        arg = urllib.urlencode(arg)
        url += arg
        res = urlfetch.fetch(url).content
        j = json.loads(res)
        Content = j['translation'][0]
        try:
            tmp = '释义：'
            tmp += ','.join(j['basic']['explains'])
            Content += '\n' + tmp
        except Exception:
            pass
        memcache.add(key = keyword, value = Content, namespace = 'dict')
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    return answerYoudao(ToUserName, FromUserName, CreateTime, MsgType, Content)