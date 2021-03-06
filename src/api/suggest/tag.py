'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp
from model import Tag as TagModel

class Tag(webapp.RequestHandler):
    def get(self,format="json"):
        
        query = self.request.get("q").lower()
        if len(query) == 0:
            simplewebapp.formatResponse(format,self,[])
            return
        
        resultedTags = []
        
        tags = TagModel.all().run()
        for tag in tags:
            if tag.name.startswith(query):
                resultedTags.append(tag.name)
                
        simplewebapp.formatResponse(format,self,resultedTags)
        