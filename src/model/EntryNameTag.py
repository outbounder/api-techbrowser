'''
Created on Dec 3, 2010

@author: outbounder
'''

from google.appengine.ext import db
from Owner import Owner

class NameTag(db.Expando):
    name = db.StringProperty()
    owner = db.ReferenceProperty(Owner)
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)

class NameProposal(db.Expando):
    owner = db.ReferenceProperty(Owner)
    name = db.StringProperty()
    raters = db.ListProperty(db.Key)
    anonymousRaters = db.IntegerProperty()
    
def saveNameTag(tagname, owner):
    q = NameTag.all().filter("name = ", tagname).fetch(1)
    
    if len(q) == 0 and len(tagname) > 0:
        if owner != None:
            t = NameTag(name=tagname, owner=owner)
            t.put()
        else:
            t = NameTag(name=tagname)
            t.put()
        return True
    else:
        return False
    
def getNameTagKeys(owner, tagsRawArray):
    tagKeys = []
    for t in tagsRawArray:
        tagMatch = NameTag.all().filter("name =", t).fetch(1)
        if len(tagMatch) == 1:
            tagKeys.append(tagMatch[0].key())
        else:
            tp = NameProposal.all().filter("name = ", t).fetch(1)
            if len(tp) == 1:
                if owner != None:
                    found = False
                    for i in tp[0].raters:
                        if i == owner:
                            found = True
                            
                    if not found:
                        tp[0].raters.append(owner.key())
                else:
                    if tp[0].anonymousRaters == None:
                        tp[0].anonymousRaters = 0
                    tp[0].anonymousRaters += 1
                    
                tp[0].put()
                    
                if len(tp[0].raters) + tp[0].anonymousRaters > 3:
                    if saveNameTag(tp[0].name, tp[0].owner) == False:
                        return False
            else:
                tp = NameProposal(owner=owner, name = t, raters = [], anonymousRaters = 0)
                tp.put()
                
    return tagKeys