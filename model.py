from google.appengine.ext import db

class Msg(db.Model):
    ToUserName = db.StringProperty()

class TopTenTopic(db.Model):
    url = db.StringProperty()
    title = db.StringProperty()
    authorPic = db.StringProperty()
    rank = db.IntegerProperty()