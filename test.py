import webapp2
from func import *
import topten

class TestTopTenHandler(webapp2.RequestHandler):
    def post(self):
        x = self.request.body
        ToUserName, FromUserName, CreateTime, MsgType, Content = parseTextXml(x)
        ToUserName, FromUserName = FromUserName, ToUserName
        self.response.write(topten.answer(ToUserName, FromUserName, CreateTime, MsgType, Content))

app = webapp2.WSGIApplication([
    ('/test/10', TestTopTenHandler)
], debug = True)