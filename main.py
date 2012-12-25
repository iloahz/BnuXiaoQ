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
        ToUserName, FromUserName, CreateTime, MsgType, Content = parseTextXml(self.request.body)
        logging.info('Received message "{}" from "{}" at "{}"'.format(Content, FromUserName, CreateTime))

        self.response.write(genTextXml(ToUserName = FromUserName,
                                       FromUserName = ToUserName,
                                       CreateTime = CreateTime,
                                       MsgType = MsgType,
                                       Content = 'You said "'.encode('utf-8') + Content + '"'.encode('utf-8'),
                                       FuncFlag = '0'))

app = webapp2.WSGIApplication([
    ('/', IndexHandler)
], debug = True)