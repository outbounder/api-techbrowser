'''
Created on Dec 3, 2010

@author: outbounder
'''
from google.appengine.ext import db
from TagProposal import TagProposal
from Entry import Entry
from TagMismatch import TagMismatch

from libs.rest.Urllib2Adapter import Resource
resource = Resource()

import re
from sets import Set

from libs.beautifulsoup.BeautifulSoup import BeautifulSoup

class Tag(db.Expando):
    name = db.StringProperty()
    createdAt = db.DateTimeProperty(auto_now_add=True)
    updatedAt = db.DateTimeProperty(auto_now=True)
    
    def create(self, tagname):
        q = db.GqlQuery("SELECT * FROM Tag WHERE name = :1 LIMIT 1", tagname).fetch(1)
        
        if len(q) == 0 and len(tagname) > 0:
            t = Tag(name=tagname)
            t.put()
            return t
        else:
            return q[0]
    
    def getByTagname(self, tagname):
        r = db.GqlQuery("SELECT * FROM Tag WHERE name = :1", tagname).fetch(1)
        if len(r) > 0:
            return r[0]
        else:
            return None

    def getTagKeys(self, tagsRawArray):
        r = db.GqlQuery("SELECT * FROM Tag WHERE name IN :1", tagsRawArray).run()
        if len(r) > 0:
            result = []
            for t in r:
                result.append(t.name)
            return result
        else:
            return []
    
    def registerTags(self, tagsRawArray):
        for t in tagsRawArray:
            tagMatch = Tag.getByTagname(t)
            if tagMatch == None:
                tp = TagProposal.getByTagname(t)
                if tp != None:
                    if tp.anonymousRaters == None:
                        tp.anonymousRaters = 0
                    else:
                        tp.anonymousRaters += 1
                        
                    tp.put()
                        
                    if len(tp.raters) + tp.anonymousRaters > 0:
                        tp = Tag.create(tp.name)
                else:
                    tp = TagProposal.create(t)
    

    def getTagsForText(self, text):
        result = []
        tags = Tag.all()
        for tag in tags:
            if re.search(r'\b'+re.escape(tag.name)+r'\b',text):
                result.append(tag.name)
        
        result = TagMismatch.excludeMismatches(result)
        
        return result
    
    def getTagsForUrl(self, url):
        try:
            content = resource.get(url).decodeBody().lower()
        except:
            content = ""
        
        soup = BeautifulSoup(content) 
        texts = soup.findAll(text=True)
    
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element)):
                return False
            return True
        
        visible_texts = filter(visible, texts)
        visibleText = " ".join(visible_texts)
        
        result = Tag.getTagsForText(visibleText)
        
        # append already defined tags for given url
        entry = Entry.all().filter("url =", url).fetch(1)
        if len(entry) > 0:
            entryStableTags = entry[0].tags
            for t in entryStableTags:
                found = False
                name = Tag.get(t).name
                for r in result:
                    if name == r:
                        found = True
                if not found:
                    result.append(name)
                    
        return result
    
    def findRelatedTags(self, tagsRaw):
        entries = Entry.all().filter("tagsRaw IN ",tagsRaw).run()
        results = Set()
        for r in entries:
            for rt in r.tagsRaw:
                if not rt in tagsRaw:
                    results.add(rt)
                    
        return sorted(results)
    
    def listStartingWith(self, query):
        resultedTags = []
        tags = Tag.all().run()
        for tag in tags:
            if tag.name.startswith(query):
                resultedTags.append(tag.name)
        return resultedTags