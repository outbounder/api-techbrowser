'''
Created on Oct 12, 2010

@author: outbounder
'''

import simplewebapp
from google.appengine.ext import webapp
from google.appengine.ext import db
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

        
        query = db.GqlQuery("SELECT * FROM Entry WHERE owners = :1", owner.key()) # how to search in owners?
        ownEntries = query.run()
        tagsRaw = getTagTerms(q)
        results = [] 
        if len(q) == 0:
            results = findEntries(ownEntries, tagsRaw)
        simplewebapp.formatResponse(format, self, results)