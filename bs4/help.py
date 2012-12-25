from func import *

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = '''Send '10' : top 10 topics on oiegg.com;
Send 'j2'(or 'ysl')
'''
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content, '0')