from google.appengine.ext import db

class Owner(db.Expando):
    uid = db.StringProperty()
    source = db.StringProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    tags = db.ListProperty(db.Key)
    
class Entry(db.Expando):
    url = db.StringProperty()
    owners = db.ListProperty(Owner)
    tagsRaw = db.StringListProperty()
    tags = db.ListProperty(db.Key)
    nameRaw = db.StringListProperty()
    names = db.ListProperty(db.Key)
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
    
class NameProposal(db.Expando):
    owner = db.ReferenceProperty(Owner)
    name = db.StringProperty()
    raters = db.ListProperty(db.Key)
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
    
def getTagKeys(owner,tagsRawArray,proposalType):
    tagKeys = []
    for t in tagsRawArray:
        tagMatch = Tag.all().filter("name =", t).fetch(1)
        if len(tagMatch) == 1:
            tagKeys.append(tagMatch[0].key())
        else:
            tp = proposalType.all().filter("name = ", t).fetch(1)
            if len(tp) == 1:
                if owner != None:
                    found = False
                    for i in tp[0].raters:
                        if i == owner:
                            found = True
                            
                    if not found:
                        tp[0].raters.append(owner)
                else:
                    if tp[0].anonymousRaters == None:
                        tp[0].anonymousRaters = 0
                    tp[0].anonymousRaters += 1
                    
                if len(tp[0].raters) > 3 or tp[0].anonymousRaters > 6:
                    if saveTag(tp[0].name, tp[0].owner) == False:
                        return False
            else:
                tp = proposalType(owner=owner, name = t)
                tp.put()
    return tagKeys
    
def saveEntry(url, sourceUUID, ownerUID, tagsList, namesList):
    r = Entry.all().filter("url =", url).fetch(1)
    o = Owner.all().filter("uid =", ownerUID).fetch(1)
    
    owner = None
    if len(o) == 0 and len(ownerUID) > 0:
        if not len(sourceUUID) > 0:
            sourceUUID = ownerUID 
        owner = Owner(uid=ownerUID, source=sourceUUID)
        owner.put()
        
    tags = getTagKeys(owner, tagsList, TagProposal)
    names = getTagKeys(owner, namesList, NameProposal)
    
    if len(r) == 0:
        e = Entry(owners=[owner], tagsRaw=tagsList, namesRaw=namesList, url=url, tags=tags, names=names)
        e.put();
        return True
    else:
        for n in names:
            found = False
            for i in r[0].names:
                if n == i:
                    found = True
            if not found:
                r[0].names.append(n)
        r[0].owners.append(owner);
        return True
    
    return False