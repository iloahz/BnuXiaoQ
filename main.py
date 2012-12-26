import webapp2
from func import *
import topten
import help
import library

def defaultAnswer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = 'miao~~XiaoQ can\'t understand that, you naughtie'
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)

def saveMsgLog(fromUser, req, res):
    m = MessageLog(fromUser, req, res)
    m.save()
    u = getOrCreateUserById(fromUser)
    u.msgCount += 1
    u.save()

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
        Content = Content.lower()
        logging.info('Received message "{}" from "{}"'.format(Content, FromUserName))
        res = None
        if Content == 'h':
            res = help.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        elif Content == '10':
            res = topten.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        elif Content.startswith('b '):
            res = library.answer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        else:
            try:
                res = library.answer(ToUserName, FromUserName, CreateTime, MsgType, 'b ' + Content, True)
            except Exception:
                res = defaultAnswer(ToUserName, FromUserName, CreateTime, MsgType, Content)
        saveMsgLog(FromUserName, x, res)
        self.response.write(res)

app = webapp2.WSGIApplication([
    ('/', IndexHandler)
], debug = True)