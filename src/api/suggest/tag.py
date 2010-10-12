'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp
from model import getAllTags

class Tag(webapp.RequestHandler):
    def get(self,format="json"):
        query = self.request.get("q")
        
        resultedTags = []
        
        tags = getAllTags()
        for tag in tags:
            if tag.name.startswith(query):
                resultedTags.append(tag.name)
                
        simplewebapp.formatResponse(format,self,resultedTags)
        