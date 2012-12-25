from google.appengine.ext import db

class Msg(db.Model):
    ToUserName = db.StringProperty()