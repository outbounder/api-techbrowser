'''
Created on Dec 3, 2010

@author: outbounder
'''
from google.appengine.ext import db
from Owner import Owner

from EntryTag import Tag
from EntryTag import saveTag
from EntryTag import TagProposal
from EntryTag import getTagKeys

from EntryNameTag import NameTag
from EntryNameTag import saveNameTag
from EntryNameTag import NameProposal
from EntryNameTag import getNameTagKeys

class Entry(db.Expando):
    url = db.StringProperty()
    owners = db.ListProperty(db.Key)
    tagsRaw = db.StringListProperty()
    tags = db.ListProperty(db.Key)
    namesRaw = db.StringListProperty()
    names = db.ListProperty(db.Key)
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)

def saveEntry(url, sourceUUID, ownerUID, tagsList, namesList):
    r = Entry.all().filter("url =", url).fetch(1)
    o = Owner.all().filter("uid =", ownerUID).fetch(1)
    
    owner = None
    if len(o) == 0 and len(ownerUID) > 0:
        if not len(sourceUUID) > 0:
            sourceUUID = ownerUID 
        owner = Owner(uid=ownerUID, source=sourceUUID)
        owner.put()
        
    tags = getTagKeys(owner, tagsList)
    names = getNameTagKeys(owner, namesList)
    
    if len(r) == 0:
        owners = []
        if owner != None:
            owners = [owner.key()]
            
        e = Entry(owners=owners, tagsRaw=tagsList, namesRaw=namesList, url=url, tags=tags, names=names)
        e.put()
            
        return True
    else:
        for n in namesList:
            found = False
            for i in r[0].namesRaw:
                if n == i:
                    found = True
            if not found:
                r[0].namesRaw.append(n)
                
        for n in names:
            found = False
            for i in r[0].names:
                if n == i:
                    found = True
            if not found:
                r[0].names.append(n)
                
        for n in tagsList:
            found = False
            for i in r[0].tagsRaw:
                if n == i:
                    found = True
            if not found:
                r[0].tagsRaw.append(n)
                
        for n in tags:
            found = False
            for i in r[0].tags:
                if n == i:
                    found = True
            if not found:
                r[0].tags.append(n)
        
        found = False
        for n in r[0].owners:
            if n == owner:
                found = True
        if not found and owner != None:        
            r[0].owners.append(owner.key());
            
        r[0].put()
            
        return True
    
    return False