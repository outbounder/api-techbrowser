'''
Created on May 14, 2010

@author: outbounder
'''

import simplewebapp
from google.appengine.ext import webapp
from google.appengine.ext import db
from model import Entry
from model import getTagTerms
from sets import Set


def findEntries(entries, queryTags):
    results = Set()
    for r in entries:
        for rt in r.tagsRaw:
            if not rt in queryTags:
                results.add(rt)
                
    return sorted(results)

class SearchTags(webapp.RequestHandler):
    
    def get(self, format="json"):
        results = []
        
        tagsRaw = getTagTerms(self.request.get("q").lower())
        
        if len(tagsRaw) == 0 or tagsRaw[0] == "": 
            simplewebapp.formatResponse(format, self, results)
            return
        
        entries = Entry.all().filter("tagsRaw IN ",tagsRaw).run()
        results = findEntries(entries, tagsRaw)

        simplewebapp.formatResponse(format, self, results)