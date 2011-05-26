'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
from libs import simplewebapp
from model import Tag

class ListStartingWith(webapp.RequestHandler):
    def get(self,format="json"):
        
        query = self.request.get("q").lower()
        if len(query) == 0:
            simplewebapp.formatResponse(format,self,[])
            return
        
        simplewebapp.formatResponse(format,self,Tag.listStartingWith(query))