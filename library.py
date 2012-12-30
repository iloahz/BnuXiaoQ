from func import *
import urllib
from google.appengine.api import memcache

def validate(c):
    if c.startswith('b ') or c.startswith('lib '):
        return True
    return False

def packBook(title, author, index, pub, year, isbn, left, Simple):
    r = ''
    r += title + '\n'
    r += author + '\n'
    r += index + '\n'
    if not Simple:
        r += pub + '\n'
    if not Simple:
        r += year + '\n'
#    r += isbn + '\n'
    r += left + '\n'
    if not Simple:
        r += '==================\n'
    else:
        r += '\n'
    return r

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content, Simple = True):
    keyword = ' '.join(Content.split()[1:])
    Content = memcache.get(key = keyword, namespace = 'lib')
#    print Content
    if not Content:
        #get data from lib.bnu.edu.cn
        url = 'http://opac.lib.bnu.edu.cn:8080/F/'
        res = urlfetch.fetch(url).content
        url = res[res.index('http://opac.lib.bnu.edu.cn:8080/F/'):res.rindex('?') + 1]
        arg = {
            'func' : 'find-b',
            'find_code' : 'WRD',
            'request' : keyword,
            'local_base' : 'BNU03',
            'adjacent' : 'Y'
        }
        arg = urllib.urlencode(arg)
        url += arg
        res = urlfetch.fetch(url).content
        soup = BeautifulSoup(res)
        Content = ''
        for i in soup.findAll('table', attrs = {'class' : 'items'}):
            try:
                title = i.find('div', attrs = {'class' : 'itemtitle'}).find('a').get_text()
                j = i.findAll('tr')
                k = j[0].find('td', attrs = {'class' : 'content'})
                s = k.get_text()
                l = []
                for t in k.stripped_strings:
                    l.append(t)
                author = l[0]
                index = l[2]
                pub = l[4]
                year = l[6]
                isbn = l[10]
                left = ' '.join(l[13].split())
                Content += packBook(title, author, index, pub, year, isbn, left, Simple)
            except Exception:
                pass
            if len(Content) >= 512:
                Content += 'More at http://m.lib.bnu.edu.cn'
                break
        if Content == '':
            url = url[0:url.index('?') + 1]
#            print url
            arg = {
                'func' : 'short',
            }
            arg = urllib.urlencode(arg)
            url += arg
            res = urlfetch.fetch(url).content
#            print res
            soup = BeautifulSoup(res)
            for i in soup.findAll('table', attrs = {'class' : 'items'}):
                try:
                    title = i.find('div', attrs = {'class' : 'itemtitle'}).find('a').get_text()
                    j = i.findAll('tr')
                    k = j[0].find('td', attrs = {'class' : 'content'})
                    s = k.get_text()
                    l = []
                    for t in k.stripped_strings:
                        l.append(t)
                    author = l[0]
                    index = l[2]
                    pub = l[4]
                    year = l[6]
                    isbn = l[10]
                    left = ' '.join(l[13].split())
                    Content += packBook(title, author, index, pub, year, isbn, left, Simple)
                except Exception:
                    pass
                if len(Content) >= 512:
                    Content += 'More at http://m.lib.bnu.edu.cn'
                    break
        memcache.add(key = keyword, value = Content, namespace = 'lib')
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)