'''
Created on Oct 12, 2010

@author: outbounder
'''

import simplewebapp
from google.appengine.ext import webapp
from model import Entry
from model import getTagTerms
from model import Owner

def findEntries(entries, queryTags):
    results = []
    for r in entries:
        for t in queryTags:
            found = False
            for rt in r.tagsRaw:
                if rt.startswith(t):
                    found = True
                    results.append({'url':r.url, 'tags':r.tagsRaw})
                    break
            if found:
                break
    return results

class Search(webapp.RequestHandler):
    
    def get(self, format="json"):
        results = []
        
        tagsRaw = getTagTerms(self.request.get("q").lower())
        # improve bellow
        if len(tagsRaw) == 0 or tagsRaw[0] == "": 
            simplewebapp.formatResponse(format, self, results)
            return
        
        entries = Entry.all().run()
        results = findEntries(entries, tagsRaw)
                
        simplewebapp.formatResponse(format, self, results)

class SearchOwn(webapp.RequestHandler):
    
    def get(self, ownerUID, format="json"):
        
        if len(ownerUID) == 0:
            simplewebapp.formatResponse(format, self, "FAILED")
            return
        
        o = Owner.all().filter("uid =", ownerUID).fetch(1)
        if len(o) == 0:
            simplewebapp.formatResponse(format, self, "FAILED")
            return
        
        owner = o[0]
        
        q = self.request.get("q").lower()
        if len(q) != 0:
            tagsRaw = getTagTerms(q)
            entries = Entry.all().filter("owner = ", owner.key()).run()
            results = findEntries(entries, tagsRaw)
            
            simplewebapp.formatResponse(format, self, results)
        else:
            entries = Entry.all().filter("owner = ", owner.key()).run()
            results = []
            for r in entries:
                results.append({'url':r.url, 'tags':r.tagsRaw})
                
            simplewebapp.formatResponse(format, self, results)
