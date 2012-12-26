#-*- encoding: utf-8 -*-

from func import *

def validate(c):
    if c == 'h':
        return True
    return False

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = '''输入“10”查看当前蛋蛋十大话题
输入“b 书名”查询图书馆图书
'''
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content, '0')