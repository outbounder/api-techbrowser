'''
Created on Dec 3, 2010

@author: outbounder
'''
from google.appengine.ext import db
from Owner import Owner

from EntryTag import registerTags 
from EntryTag import getTagKeys
from EntryTag import Tag

class Entry(db.Expando):
    url = db.StringProperty()
    owners = db.ListProperty(db.Key)
    tagsRaw = db.StringListProperty()
    tags = db.ListProperty(db.Key)
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)

def saveEntry(url, sourceUUID, ownerUID, tagsList, name):
    r = Entry.all().filter("url =", url).fetch(1)
    o = Owner.all().filter("uid =", ownerUID).fetch(1)
    
    owner = None
    if len(o) == 0 and len(ownerUID) > 0:
        if not len(sourceUUID) > 0:
            sourceUUID = ownerUID 
        owner = Owner(uid=ownerUID, source=sourceUUID)
        owner.put()
        
    registerTags(owner, tagsList)
        
    if len(r) == 0:
        owners = []
        if owner != None:
            owners = [owner.key()]
            
        tags = getTagKeys(owner, tagsList)
            
        e = Entry(owners=owners, url=url, tagsRaw=tagsList, tags=tags)
        e.put()
            
        return True
    else:
        # TODO implement entry's tags update logic 
        found = False
        for n in r[0].owners:
            if n == owner:
                found = True
        if not found and owner != None:        
            r[0].owners.append(owner.key());
            
        r[0].put()
        return True
    
    return False