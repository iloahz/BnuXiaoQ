from func import *
import urllib
from google.appengine.api import memcache
import json

def validate(c):
    if c.startswith('d '):
        return True
    return False

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content, Simple = True):
    keyword = ' '.join(Content.split()[1:])
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
    Content = memcache.get(key = keyword, namespace = 'dict')
    if not Content:
        #get data from baidu
        url = 'http://openapi.baidu.com/public/2.0/bmt/translate?'
        arg = {
            'client_id' : 'Tx2FORF0UyXaENR9A4OnmD8B',
            'q' : keyword,
        }
        arg = urllib.urlencode(arg)
        url += arg
        res = urlfetch.fetch(url).content
        j = json.loads(res)
        Content = j['trans_result'][0]['dst']
        memcache.add(key = keyword, value = Content, namespace = 'dict')
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