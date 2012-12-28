from func import *
import urllib
from google.appengine.api import memcache

def validate(c):
    if c.startswith('b '):
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
    Content = memcache.get(key = keyword, namespace = 'lib')
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
            'adjacent' : 'Y',
        }
        arg = urllib.urlencode(arg)
        url += arg
        res = urlfetch.fetch(url).content
        soup = BeautifulSoup(res)
        soup = soup.findAll('table', attrs = {'class' : 'items'})
        Content = ''
        for i in soup:
            title = i.find('div', attrs = {'class' : 'itemtitle'}).find('a').get_text()
    #        url = i.find('div', attrs = {'class' : 'itemtitle'}).find('a').get('href')
            j = i.findAll('tr')
            k = j[0].find('td', attrs = {'class' : 'content'})
            s = k.get_text()
            l = []
            for t in k.stripped_strings:
                l.append(t)
            try:
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