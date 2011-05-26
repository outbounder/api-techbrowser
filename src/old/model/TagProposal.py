'''
Created on May 17, 2011

@author: outbounder
'''
from google.appengine.ext import db

class TagProposal(db.Expando):
    name = db.StringProperty()
    raters = db.ListProperty(db.Key) # owner keys
    anonymousRaters = db.IntegerProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
    def create(self, tagname):
        q = db.GqlQuery("SELECT * FROM TagProposal WHERE name = :1 LIMIT 1", tagname).fetch(1)
        
        if len(q) == 0 and len(tagname) > 0:
            t = TagProposal(name=tagname)
            t.raters = []
            t.anonymousRaters = 0
            t.put()
            return t
        else:
            q[0].name = tagname
            return q[0]
        
    def getByTagname(self, tagname):
        r = db.GqlQuery("SELECT * FROM TagProposal WHERE name = :1", tagname).fetch(1)
        if len(r) > 0:
            return r[0]
        else:
            return None