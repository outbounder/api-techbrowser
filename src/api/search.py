'''
Created on Oct 12, 2010

@author: outbounder
'''

import simplewebapp
from google.appengine.ext import webapp
from model import getMockupSearchResults

class Search(webapp.RequestHandler):
    
    def get(self,format="json"):
        # do search based on query to the external datastorage
        # if search results are found record the query
        simplewebapp.formatResponse(format,self,getMockupSearchResults())
        