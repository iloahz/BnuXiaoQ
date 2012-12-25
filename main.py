import webapp2
from func import *

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
        logging.info('Received message "{}" from "{}" at "{}"'.format(Content, FromUserName, CreateTime))
        res = 'Don\'t know what you are saying...'
        res = genTextXml(ToUserName = FromUserName,
                         FromUserName = ToUserName,
                         CreateTime = CreateTime,
                         MsgType = MsgType,
                         Content = 'You said "' + Content + '"',
                         FuncFlag = '0')
        self.response.write(res)

app = webapp2.WSGIApplication([
    ('/', IndexHandler)
], debug = True)