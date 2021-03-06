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

class SearchEntries(webapp.RequestHandler):
    
    def get(self, format="json"):
        results = []
        
        tagsRaw = getTagTerms(self.request.get("q").lower())
        
        if len(tagsRaw) == 0 or tagsRaw[0] == "": 
            simplewebapp.formatResponse(format, self, results)
            return
        
        # EXTREMELY SLOW ! OPTIMIZE!
        entries = Entry.all().order("-updatedAt").run()
        results = findEntries(entries, tagsRaw)
                
        simplewebapp.formatResponse(format, self, results)

class SearchOwn(webapp.RequestHandler):
    
    def get(self, ownerUID, format="json"):
        
        if len(ownerUID) == 0:
            simplewebapp.formatResponse(format, self, "FAILED")
            return
        
        o = Owner.all().filter("uid =", ownerUID).fetch(1)
        if len(o) != 1:
            simplewebapp.formatResponse(format, self, "FAILED")
            return
        
        owner = o[0]
        
        q = self.request.get("q").lower()
        
        # VEERY SLOW ! OPTIMIZE!
        ownEntries = db.GqlQuery("SELECT * FROM Entry WHERE owners = :1", owner).run()
        tagsRaw = getTagTerms(q)
        results = [] 
        if len(q) != 0:
            results = findEntries(ownEntries, tagsRaw)
        simplewebapp.formatResponse(format, self, results)