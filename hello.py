#-*- encoding: utf-8 -*-

from func import *

def validate(c):
    if c == 'Hello2BizUser'.lower():
        return True
    return False

def answer(ToUserName, FromUserName, CreateTime, MsgType, Content):
    Content = '''Hi，我是 师大小Q，谢谢你收留我~
输入“h”可以查看帮助哦~~
'''
    return genTextXml(ToUserName, FromUserName, CreateTime, MsgType, Content)