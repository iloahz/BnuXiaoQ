from func import *

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = '''Send '10' to get the top 10 topics on oiegg.com;
Send 'book name' to look up it in our library;
'''
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content, '0')