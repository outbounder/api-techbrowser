from google.appengine.ext import db

class Owner(db.Expando):
    uid = db.StringProperty()
    source = db.StringProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    tags = db.ListProperty(db.Key)
    
class Entry(db.Expando):
    owner = db.ReferenceProperty(Owner)
    url = db.StringProperty()
    tagsRaw = db.StringListProperty()
    tags = db.ListProperty(db.Key)
    raters = db.ListProperty(db.Key) # owner keys
    anonymousDuplicatesCount = db.IntegerProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
class Tag(db.Expando):
    name = db.StringProperty()
    owner = db.ReferenceProperty(Owner)
    followups = db.ListProperty(db.Key) # owner keys
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
class TagProposal(db.Expando):
    owner = db.ReferenceProperty(Owner)
    name = db.StringProperty()
    raters = db.ListProperty(db.Key) # owner keys
    anonymousRaters = db.IntegerProperty()
    
def getTagTerms(tagsLine):
    if len(tagsLine) > 0:
        return tagsLine.split(" ") # TODO improve
    else:
        return []

def saveTag(tagname, ownerUID):
    q = Tag.all().filter("name = ", tagname).fetch(1)
    o = Owner.all().filter("uid =", ownerUID).fetch(1)
    if len(q) == 1 and len(o) == 1:
        q[0].followups.append(o[0].key())
        q[0].put()
        return True
    elif len(q) == 0 and len(tagname) > 0:
        if len(o) == 1:
            t = Tag(name=tagname, owner=o[0])
            t.put()
        else:
            t = Tag(name=tagname)
            t.put()
        return True
    else:
        return False
    
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
    
def rateEntry(entry, owner=None):
    if owner != None:
        if entry.raters.index(owner.key()) == -1:
            entry.raters.append(owner.key())
    else:
        if entry.anonymousDuplicatesCount == None:
            entry.anonymousDuplicatesCount = 0
        entry.anonymousDuplicatesCount += 1
    entry.put();
    
def saveEntry(url, sourceUUID, ownerUID, tagsRaw):
    r = Entry.all().filter("url =", url).fetch(1)
    o = Owner.all().filter("uid =", ownerUID).fetch(1)
    owner = None
    if len(o) == 0 and len(ownerUID) > 0:
        if not len(sourceUUID) > 0:
            sourceUUID = ownerUID 
        owner = Owner(uid=ownerUID, source=sourceUUID)
        owner.put()
        
    tags = []
    for t in tagsRaw:
        tag = Tag.all().filter("name =", t).fetch(1)
        if len(tag) == 1:
            tags.append(tag[0].key())
        else:
            tp = TagProposal.all().filter("name = ", t).fetch(1)
            if len(tp) == 1:
                if owner != None:
                    tp[0].raters.append(owner)
                else:
                    if tp[0].anonymousRaters == None:
                        tp[0].anonymousRaters = 0
                    tp[0].anonymousRaters += 1
                    
                if len(tp[0].raters) > 3 or tp[0].anonymousRaters > 6:
                    if saveTag(tp[0].name, tp[0].owner) == False:
                        return False
            else:
                tp = TagProposal(owner=owner, name = t)
                tp.put()
    
    if len(r) == 0:
        if owner != None:    
            e = Entry(owner=owner, tagsRaw=tagsRaw, url=url, tags=tags)
            e.put();
        else:
            e = Entry(tagsRaw=tagsRaw, url=url, tags=tags)
            e.put()
        return True
    else:
        if owner != None:
            rateEntry(r[0], owner)
        else:
            rateEntry(r[0])
        return True
    
    return False