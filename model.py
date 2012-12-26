from google.appengine.ext import db

class Msg(db.Model):
    ToUserName = db.StringProperty()

class TopTenTopic(db.Model):
    url = db.StringProperty()
    title = db.StringProperty()
    authorPic = db.StringProperty()
    rank = db.IntegerProperty()

class User(db.Model):
    wechatId = db.StringProperty()
    msgCount = db.IntegerProperty(default = 0)
    createDate = db.DateTimeProperty(auto_now_add = True)

class MessageLog(db.Model):
    fromUser = db.ReferenceProperty(User)
    req = db.StringProperty()
    res = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add = True)