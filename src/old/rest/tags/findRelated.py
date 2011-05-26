'''
Created on May 14, 2010

@author: outbounder
'''

from libs import simplewebapp
from google.appengine.ext import webapp
from model import Tag

class FindRelated(webapp.RequestHandler):
    
    def get(self, format="json"):
        results = []
        
        tagsRaw = self.request.get("q").lower().split(" ")
        
        if len(tagsRaw) == 0 or tagsRaw[0] == "": 
            simplewebapp.formatResponse(format, self, results)
            return
        
        results = Tag.findRelatedTags(tagsRaw) 

        simplewebapp.formatResponse(format, self, results)