'''
Created on Dec 3, 2010

@author: outbounder
'''
from google.appengine.ext import db
from Owner import Owner
from model.aetycoon import PickleProperty

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
    
class TagMismatch(db.Expando):
    owner = db.ReferenceProperty(Owner)
    name = db.StringProperty()
    withTags = PickleProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
def saveTag(tagname, owner):
    q = db.GqlQuery("SELECT * FROM Tag WHERE name = :1 LIMIT 1", tagname).fetch(1)
    
    if len(q) == 0 and len(tagname) > 0:
        t = Tag(name=tagname)
        t.owner = owner
        t.put()
        return t
    else:
        return q[0]
    
def saveTagProposal(tagname, owner):
    q = db.GqlQuery("SELECT * FROM TagProposal WHERE name = :1 LIMIT 1", tagname).fetch(1)
    
    if len(q) == 0 and len(tagname) > 0:
        t = TagProposal(name=tagname)
        t.owner = owner
        t.raters = []
        t.anonymousRaters = 0
        t.put()
        return t
    else:
        q[0].owner = owner
        q[0].name = tagname
        return q[0]
    
def saveTagMismatch(tagname, tags, owner):
    q = db.GqlQuery("SELECT * FROM TagMismatch WHERE name = :1 LIMIT 1", tagname).fetch(1)
    
    owner = None
    if len(q) == 0:
        tagMismatch = TagMismatch(name=tagname)
        tagMismatch.owner = owner
        tagMismatch.withTags = dict()
        for tag in tags:
            if not tag == tagname:
                tagMismatch.withTags[tag] = 1
        tagMismatch.put()
        return tagMismatch
    else:
        q[0].owner = owner
        q[0].name = tagname
        for t in tags:
            if not q[0].withTags.has_key(t):
                q[0].withTags[t] = 1
            else:
                q[0].withTags[t] += 1
        q[0].put()
        return q[0]
    
def excludeMismatches(tags):
    return [t for t in tags if isMismatchedTag(t, tags)]
        
                    
def isMismatchedTag(tagName, tags):
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
    
def getTag(tagname):
    r = db.GqlQuery("SELECT * FROM Tag WHERE name = :1", tagname).fetch(1)
    if len(r) > 0:
        return r[0]
    else:
        return None

def getTagProposal(tagname):
    r = db.GqlQuery("SELECT * FROM TagProposal WHERE name = :1", tagname).fetch(1)
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
                    
                if len(tp.raters) + tp.anonymousRaters > 0:
                    tp = saveTag(tp.name, tp.owner)
            else:
                tp = saveTagProposal(t, owner)
    
def getTagKeys(tagsRawArray):
    tagKeys = []
    for t in tagsRawArray:
        tagMatch = getTag(t)
        if tagMatch != None:
            tagKeys.append(tagMatch.key())
                
    return tagKeys