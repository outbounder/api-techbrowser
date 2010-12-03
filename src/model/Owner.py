'''
Created on Dec 3, 2010

@author: outbounder
'''
from google.appengine.ext import db

class Owner(db.Expando):
    uid = db.StringProperty()
    source = db.StringProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    tags = db.ListProperty(db.Key)
    
def saveOwner(uid, source):
    q = Owner.all().filter("uid =", uid).count(1)
    if q == 0 and len(source) > 0:
        o = Owner(uid=uid, source=source)
        o.put()
        return True
    else:
        return False
    
def deleteOwner(uid, source):
    q = Owner.all().filter("uid =", uid).filter("source =", source).fetch(1)
    if len(q) != 0:
        q[0].delete()
        return True
    else:
        return False