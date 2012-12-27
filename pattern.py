from func import *

def validate(c):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', c).get()
    if p:
        return True
    return False

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    p = db.GqlQuery('SELECT * FROM Pattern WHERE input = :1', Content).get()
    Content = p.output
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)