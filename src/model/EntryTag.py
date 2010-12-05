'''
Created on Dec 3, 2010

@author: outbounder
'''
from google.appengine.ext import db
from Owner import Owner
from aetycoon import DerivedProperty

class Tag(db.Expando):
    parents = db.ListProperty(db.Key)
    parents_count = DerivedProperty(lambda self: len(self.parents))
    owner = db.ReferenceProperty(Owner)
    name = db.StringProperty()
    childs = db.ListProperty(db.Key)
    childs_count = DerivedProperty(lambda self: len(self.parents))
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
class TagProposal(db.Expando):
    parents = db.ListProperty(db.Key)
    parents_count = DerivedProperty(lambda self: len(self.parents))
    owner = db.ReferenceProperty(Owner)
    name = db.StringProperty()
    childs = db.ListProperty(db.Key)
    childs_count = DerivedProperty(lambda self: len(self.parents))
    raters = db.ListProperty(db.Key) # owner keys
    anonymousRaters = db.IntegerProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
def saveTag(tagname, owner, parent):
    q = None
    if parent != None:
        q = db.GqlQuery("SELECT * FROM Tag WHERE parents = :1 AND name = :2", parent.key(), tagname).fetch(1)
    else:
        q = db.GqlQuery("SELECT * FROM Tag WHERE parents_count = 0 AND name = :1", tagname).fetch(1)
    
    if len(q) == 0 and len(tagname) > 0:
        t = Tag(name=tagname,childs=[],parents=[])
        t.owner = owner
        if parent != None:
            t.parents = []
            t.parents.append(parent.key())
        t.put()
        
        if parent != None:
            parent.childs.append(t.key())
            parent.put()
                
        return t
    else:
        return q[0]
    
def saveTagProposal(tagname, owner, parent):
    q = None
    if parent != None:
        q = db.GqlQuery("SELECT * FROM TagProposal WHERE parents = :1 AND name = :2", parent.key(), tagname).fetch(1)
    else:
        q = db.GqlQuery("SELECT * FROM TagProposal WHERE parents_count = 0 AND name = :1", tagname).fetch(1)
    
    if len(q) == 0 and len(tagname) > 0:
        t = TagProposal(name=tagname)
        t.owner = owner
        t.raters = []
        t.anonymousRaters = 0
        if parent != None:
            t.parents = []
            t.parents.append(parent.key())
        t.put()
        
        if parent != None:
            parent.childs.append(t.key())
            parent.put()
                
        return t
    else:
        return q[0]
    
def getTag(tagname, parent):
    r = None
    if parent != None:
        r = db.GqlQuery("SELECT * FROM Tag WHERE parents = :1 AND name = :2", parent.key(), tagname).fetch(1)
    else:
        r = db.GqlQuery("SELECT * FROM Tag WHERE parents_count = 0 AND name = :1", tagname).fetch(1)
    if len(r) > 0:
        return r[0]
    else:
        return None

def getTags(parent):
    if parent != None:
        return db.GqlQuery("SELECT * FROM Tag WHERE parents = :1", parent.key()).fetch(100)
    else:
        return db.GqlQuery("SELECT * FROM Tag WHERE parents_count = 0").fetch(100)

def getTagProposal(tagname, parent):
    r = None
    if parent != None:
        r = db.GqlQuery("SELECT * FROM TagProposal WHERE parents = :1 AND name = :2", parent.key(), tagname).fetch(1)
    else:
        r = db.GqlQuery("SELECT * FROM TagProposal WHERE parents_count = 0 AND name = :1", tagname).fetch(1)
    if len(r) > 0:
        return r[0]
    else:
        return None
        
    
def registerTags(owner, tagsRawArray):
    parent = None
    for t in tagsRawArray:
        tagMatch = getTag(t, parent)
        if tagMatch == None:
            tp = getTagProposal(t, parent)
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
                    tp = saveTag(tp.name, tp.owner, parent)
                    
                parent = tp
            else:
                tp = saveTagProposal(t, owner, parent)
                parent = tp
        else:
            parent = tagMatch
    
def getTagKeys(owner, tagsRawArray):
    tagKeys = []
    parent = None
    for t in tagsRawArray:
        tagMatch = getTag(t, parent)
        if tagMatch != None:
            tagKeys.append(tagMatch.key())
            parent = tagMatch
        else:
            return tagKeys
                
    return tagKeys