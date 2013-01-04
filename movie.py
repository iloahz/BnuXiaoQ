#-*- encoding: utf-8 -*-

import webapp2
from google.appengine.api import memcache
from func import *

def validate(c):
    if c == 'dy' or c == 'cfc' or c == '175' or c == '17.5':
        return True
    return False

def answerDy(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = '''输入“cfc”查看中影电影院影讯
输入“17.5”（或“175”）查看17.5影城影讯'''
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def dump(d):
    s = ''
    for i, j in d:
        s += '影片：' + i + '\n'
        s += '票价：' + j + '\n'
        s += '场次：'
        l = d[i, j]
        l.sort()
        lst = None
        for k in l:
            if lst:
                s += ', '
            s += k
            lst = k
        s += '\n\n'
    return s

def answerByTheater(ToUserName, FromUserName, CreateTime, MsgType, Content, Theater):
    q = db.GqlQuery('SELECT * FROM Movie WHERE theater = :1', Theater)
    d = dict()
    upd = None
    for i in q.fetch(limit = 999):
        if not upd:
            upd = i.updateTime
        if (i.name, i.price) not in d:
            d[i.name, i.price] = list()
        d[i.name, i.price].append(i.startTime)
    Content = dump(d)
    Content += '更新时间：' + (upd + datetime.timedelta(hours = 8)).strftime('%m月%d日 %H:%M')
    Content += '\n更多信息请访问：http://m.douban.com/movie/recent/'
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def answerCfc(ToUserName, FromUserName, CreateTime, MsgType, Content):
    return answerByTheater(ToUserName, FromUserName, CreateTime, MsgType, Content, 'cfc')

def answer175(ToUserName, FromUserName, CreateTime, MsgType, Content):
    return answerByTheater(ToUserName, FromUserName, CreateTime, MsgType, Content, '175')

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    if Content == 'dy':
        return answerDy(ToUserName, FromUserName, CreateTime, MsgType, Content)
    elif Content == 'cfc':
        return answerCfc(ToUserName, FromUserName, CreateTime, MsgType, Content)
    else:
        return answer175(ToUserName, FromUserName, CreateTime, MsgType, Content)

def getOrCreateMovieByUid(uid):
    m = db.GqlQuery('SELECT * FROM Movie WHERE uid = :1', uid).get()
    if not m:
        m = Movie()
        m.uid = uid
        m.save()
    return m

def update175(startUid):
    url = 'http://theater.mtime.com/China_Beijing_Haidian/1786/'
    res = urlfetch.fetch(url).content
    soup = BeautifulSoup(res)
    div = soup.find('div', attrs = {'id' : 'theaterShowtimeListDiv'})
    dd = div.findAll('dd')
    cnt = 0
    theater = '175'
    for i in dd:
        name = i.find('a', attrs = {'class' : 'c_000'}).get_text()
        ul = i.find('ul', attrs = {'class' : 's_timelist clearfix __r_c_'})
        li = ul.findAll('li')
        for j in li:
            startTime = j.find('strong').get_text()
            price = j.find('em').get_text()
            m = getOrCreateMovieByUid(startUid)
            m.theater = theater
            m.name = name
            m.startTime = startTime
            m.price = price
            m.save()
            startUid += 1
            cnt += 1
    return cnt

def updateCfc(startUid):
    url = 'http://www.cfc.com.cn/'
    res = urlfetch.fetch(url).content
    res = res.decode('gbk')
    soup = BeautifulSoup(res)
    soup = soup.find('div', attrs = {'id' : 'tbx01'})
    tr = soup.findAll('tr')
    cnt = len(tr) - 1
    theater = 'cfc'
    for i in range(1, len(tr)):
        td = tr[i].findAll('td')
        name = td[0].get_text()
        startTime = td[1].get_text()
        price = td[3].get_text()
        m = getOrCreateMovieByUid(startUid)
        m.theater = theater
        m.name = name
        m.startTime = startTime
        m.price = price
        m.save()
        startUid += 1
#        print name, time, price
    return cnt

class FetchHandler(webapp2.RequestHandler):
    def get(self):
        uid = 0
        uid += update175(uid)
        uid += updateCfc(uid)

app = webapp2.WSGIApplication([
    ('/movie/fetch', FetchHandler)
], debug = True)