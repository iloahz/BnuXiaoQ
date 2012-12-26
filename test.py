from main import *

class TestTopTenHandler(webapp2.RequestHandler):
    def post(self):
        x = self.request.body
        ToUserName, FromUserName, CreateTime, MsgType, Content = parseTextXml(x)
        ToUserName, FromUserName = FromUserName, ToUserName
        self.response.write(topten.answer(ToUserName, FromUserName, CreateTime, MsgType, Content))

class TestLibHandler(webapp2.RequestHandler):
    def post(self):
        x = self.request.body
        ToUserName, FromUserName, CreateTime, MsgType, Content = parseTextXml(x)
        ToUserName, FromUserName = FromUserName, ToUserName
        self.response.write(library.answer(ToUserName, FromUserName, CreateTime, MsgType, 'b' + Content, True))

app = webapp2.WSGIApplication([
    ('/test/10', TestTopTenHandler),
    ('/test/lib', TestLibHandler)
], debug = True)