import webapp2
from func import *
import topten

def defaultAnswer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = 'miao~~'
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        s = self.request.GET['signature']
        t = self.request.GET['timestamp']
        n = self.request.GET['nonce']
        e = self.request.GET['echostr']
        if validateSource(timestamp = t, nonce = n, signature = s):
            self.response.write(e)
        else:
            self.response.write('Bad boy!')
    def post(self):
        x = self.request.body
        ToUserName, FromUserName, CreateTime, MsgType, Content = parseTextXml(x)
        ToUserName, FromUserName = FromUserName, ToUserName
        logging.info('Received message "{}" from "{}" at "{}"'.format(Content, FromUserName, CreateTime))
        res = None
        if Content == '10':
            res = topten.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        else:
            res = specialPhrase(Content)
            if not res:
                res = defaultAnswer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        self.response.write(res)

app = webapp2.WSGIApplication([
    ('/', IndexHandler)
], debug = True)