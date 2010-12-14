'''
Created on Dec 3, 2010

@author: outbounder
'''
from google.appengine.ext import db
from Owner import Owner

class Tag(db.Expando):
    owner = db.ReferenceProperty(Owner)
    name = db.StringProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
class TagProposal(db.Expando):
    owner = db.ReferenceProperty(Owner)
    name = db.StringProperty()
    raters = db.ListProperty(db.Key) # owner keys
    anonymousRaters = db.IntegerProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
def saveTag(tagname, owner):
    q = db.GqlQuery("SELECT * FROM Tag WHERE  AND name = :2 LIMIT 1", tagname).fetch(1)
    
    if len(q) == 0 and len(tagname) > 0:
        t = Tag(name=tagname)
        t.owner = owner
        t.put()
        return t
    else:
        return q[0]
    
def saveTagProposal(tagname, owner):
    q = db.GqlQuery("SELECT * FROM TagProposal WHERE name = :2 LIMIT 1", tagname).fetch(1)
    
    if len(q) == 0 and len(tagname) > 0:
        t = TagProposal(name=tagname)
        t.owner = owner
        t.raters = []
        t.anonymousRaters = 0
        t.put()
        return t
    else:
        return q[0]
    
def getTag(tagname):
    r = db.GqlQuery("SELECT * FROM Tag WHERE parents_count = 0 AND name = :1", tagname).fetch(1)
    if len(r) > 0:
        return r[0]
    else:
        return None

def getTagProposal(tagname):
    r = db.GqlQuery("SELECT * FROM TagProposal WHERE parents_count = 0 AND name = :1", tagname).fetch(1)
    if len(r) > 0:
        return r[0]
    else:
        return None
    
def registerTags(owner, tagsRawArray):
    for t in tagsRawArray:
        tagMatch = getTag(t)
        if tagMatch == None:
            tp = getTagProposal(t)
            if tp != None:
                if owner != None:
                    found = False
                    for i in tp.raters:
                        if i == owner:
                            found = True
                            
                    if not found:
                        tp.raters.append(owner.key())
                else:
                    if tp.anonymousRaters == None:
                        tp.anonymousRaters = 0
                    tp.anonymousRaters += 1
                    
                tp.put()
                    
                if len(tp.raters) + tp.anonymousRaters > 3:
                    tp = saveTag(tp.name, tp.owner)
            else:
                tp = saveTagProposal(t, owner)
    
def getTagKeys(owner, tagsRawArray):
    tagKeys = []
    for t in tagsRawArray:
        tagMatch = getTag(t)
        if tagMatch != None:
            tagKeys.append(tagMatch.key())
        else:
            return tagKeys
                
    return tagKeys