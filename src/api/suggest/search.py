'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp

from model import getAllSearchQueries
from model import getMockupSearchQuerySuggestions

class Search(webapp.RequestHandler):
    def get(self,format="json"):
        query = self.request.get("q")
        
        resultedQueries = []
        
        # this should be replaced with query to the external datastorage for suggestions
        searchQuerySuggestions = getMockupSearchQuerySuggestions()
        for sq in searchQuerySuggestions:
            if sq.startswith(query):
                resultedQueries.append(sq)
        
        # is this needed at all (?)
        searchQueries = getAllSearchQueries()
        for sq in searchQueries:
            if sq.query.startswith(query):
                resultedQueries.append(sq.query)
                
        simplewebapp.formatResponse(format,self,resultedQueries)