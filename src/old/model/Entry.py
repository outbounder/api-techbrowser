'''
Created on Dec 3, 2010

@author: outbounder
'''
from google.appengine.ext import db
from Tag import Tag

class Entry(db.Expando):
    url = db.StringProperty()
    tagsRaw = db.StringListProperty()
    tags = db.ListProperty(db.Key)
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)

    def create(self, url, tagsList):
        r = Entry.all().filter("url =", url).fetch(1)
        
        Tag.registerTags(tagsList)
            
        if len(r) == 0:
                
            tags = Tag.getTagKeys(tagsList)
                
            e = Entry(url=url, tagsRaw=tagsList, tags=tags)
            e.put()
                
            return True
        else:
            # append new rawTags
            for n in tagsList:
                found = False
                for t in r[0].tagsRaw:
                    if n == t:
                        found = True
                if not found:
                    r[0].tagsRaw.append(n)
                    
            # append new tags
            tags = Tag.getTagKeys(tagsList)
            for n in tags:
                found = False
                for t in r[0].tags:
                    if n == t:
                        found = True
                if not found:
                    r[0].tags.append(n)
                
            r[0].put()
            return True
        
        return False
    
    def matchByTags(self, queryTags):
        entries = Entry.all().order("-updatedAt").run() 
        results = []
        for r in entries:
            
            for index,t in enumerate(queryTags):
                match = False
                for rt in r.tagsRaw:
                    if rt == t and index != len(queryTags)-1:
                        match = True
                    elif rt.startswith(t):
                        match = True
                if match == False:
                    break
                    
            if match == True:
                results.append({'url':r.url, 'tagsRaw': r.tagsRaw})
            
        return results