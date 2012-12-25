import webapp2
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup
from func import *

class FetchHandler(webapp2.RequestHandler):
    def get(self):
        res = urlfetch.fetch('http://www.oiegg.com/index.php').content
        soup = BeautifulSoup(res)
        soup = soup.find('div', attrs = {'class' : 'mainbox forumlist box on-left'})
        soup = soup.findAll('li')
        for i in range(0, len(soup)):
            j = soup[i].findAll('a')[1]
            title = j.get_text()
            url = 'http://www.oiegg.com/' + j.get('href')
            t = db.GqlQuery('SELECT * FROM TopTenTopic WHERE rank = :1', i).get()
            t.url = url
            t.title = title
            t.save()
        logging.info('Top ten updated at %s', time.ctime())

app = webapp2.WSGIApplication([
    ('/topten/fetch', FetchHandler)
], debug = True)