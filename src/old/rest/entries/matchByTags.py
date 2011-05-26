'''
Created on Oct 12, 2010

@author: outbounder
'''

from libs import simplewebapp
from google.appengine.ext import webapp
from model import Entry

class MatchByTags(webapp.RequestHandler):
    
    def get(self, format="json"):
        results = []
        
        tagsRaw = self.request.get("q").lower().split(" ")
        
        if len(tagsRaw) == 0 or tagsRaw[0] == "": 
            simplewebapp.formatResponse(format, self, results)
            return
        
        # EXTREMELY SLOW ! OPTIMIZE!
        results = Entry.matchByTags(tagsRaw)
                
        simplewebapp.formatResponse(format, self, results)