import webapp2
from func import *

class InitHandler(webapp2.RequestHandler):
    def get(self):
        if not getTopTen():
            for i in range(0, 10):
                t = TopTenTopic()
                t.url = ''
                t.title = ''
                t.rank = i
                t.save()

app = webapp2.WSGIApplication([
    ('/init', InitHandler)
], debug = True)