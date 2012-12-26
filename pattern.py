from func import *

global p

def validate(c):
    global p
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', c).get()
    if p:
        return True
    return False

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    global p
    Content = p.output
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)