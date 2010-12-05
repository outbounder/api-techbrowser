'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp

from model import Tag

class Search(webapp.RequestHandler):
    def get(self, format="json"):
        
        query = self.request.get("q").lower()
        if len(query) == 0:
            simplewebapp.formatResponse(format, self, [])
            return
        
        resultedQueries = []
        
        tags = Tag.all().run()
        for st in tags:
            if st.name.startswith(query):
                resultedQueries.append(st.name)
                
        simplewebapp.formatResponse(format, self, resultedQueries)