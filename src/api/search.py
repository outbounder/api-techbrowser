'''
Created on Oct 12, 2010

@author: outbounder
'''

import simplewebapp
from google.appengine.ext import webapp
from model import getMockupSearchResults

class Search(webapp.RequestHandler):
    
    def get(self,format="json"):
        query = self.request.get("q").lower()
        
        # do search based on query to the external datastorage
        # if search results are found record the query
        results = []
        mockupResulsts = getMockupSearchResults()
        for r in mockupResulsts:
            if r['name'].find(query) != -1 or r['url'].find(query) != -1:
                results.append(r)
                
        simplewebapp.formatResponse(format,self,results)
        