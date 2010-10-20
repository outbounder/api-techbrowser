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
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
class Tag(db.Expando):
    name = db.StringProperty()
    owner = db.ReferenceProperty(Owner)
    followups = db.ListProperty(db.Key)
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
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
    elif len(q) == 0 and len(o) == 1 and len(tagname) > 0:
        t = Tag(name=tagname, owner=o[0])
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
    
def saveEntry(url, ownerUID, tagsRaw):
    r = Entry.all().filter("url =", url).fetch(1)
    o = Owner.all().filter("uid =", ownerUID).fetch(1)
    if len(r) == 0 and len(tagsRaw) > 0 and len(url) > 0:
        tags = []
        for t in tagsRaw:
            tag = Tag.all().filter("name =", t).fetch(1)
            if len(tag) == 1:
                tags.append(tag[0].key())
        
        if len(ownerUID) > 0 and len(o) == 0:
            owner = Owner(uid=ownerUID, source=ownerUID) # TODO improve
            owner.put()
            
            e = Entry(owner=owner, tagsRaw=tagsRaw, url=url, tags=tags)
            e.put()
        elif len(ownerUID) > 0 and len(o) == 1:
            e = Entry(owner=o[0], tagsRaw=tagsRaw, url=url, tags=tags)
            e.put();
        else:
            e = Entry(tagsRaw=tagsRaw, url=url, tags=tags)
            e.put()
        
        return True
    else:
        return False
