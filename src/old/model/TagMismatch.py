'''
Created on May 17, 2011

@author: outbounder
'''
from google.appengine.ext import db
from model.aetycoon import PickleProperty

class TagMismatch(db.Expando):
    name = db.StringProperty()
    withTags = PickleProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
    def create(self, tagname, tags):
        q = db.GqlQuery("SELECT * FROM TagMismatch WHERE name = :1 LIMIT 1", tagname).fetch(1)
        
        if len(q) == 0:
            tagMismatch = TagMismatch(name=tagname)
            tagMismatch.withTags = dict()
            for tag in tags:
                if not tag == tagname:
                    tagMismatch.withTags[tag] = 1
            tagMismatch.put()
            return tagMismatch
        else:
            q[0].name = tagname
            for t in tags:
                if not q[0].withTags.has_key(t):
                    q[0].withTags[t] = 1
                else:
                    q[0].withTags[t] += 1
            q[0].put()
            return q[0]
        
    def excludeMismatches(self, tags):
        return [t for t in tags if TagMismatch.isMismatchedTag(t, tags)]
    
    def isMismatchedTag(self, tagName, tags):
        r = db.GqlQuery("SELECT * FROM TagMismatch WHERE name = :1 LIMIT 1", tagName).fetch(1)
        if len(r) > 0:
            minRate = 1
            sumRate = 0
            sumHits = 0
            for k, v in r[0].withTags.iteritems():
                sumRate += v
                for it in tags:
                    if it == k:
                        sumHits += 1
                        break
            if sumHits > len(tags)/2:
                if sumRate / sumHits > minRate:
                    return False
                
        return True