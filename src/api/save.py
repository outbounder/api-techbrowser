'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp

from model import saveEntry
from model import getTagTerms

class SaveEntry(webapp.RequestHandler):
    def executeSave(self, format):
        url = self.request.get("url").lower()
        if url.find("http://") == -1 and url.find("https://") == -1:
            simplewebapp.formatResponse(format, self, "FAILED")
            return
        
        tags = getTagTerms(self.request.get("tags").lower())
        names = getTagTerms(self.request.get("names").lower())
        owner = self.request.get("owner").lower()
        source = self.request.get("source").lower()
        if saveEntry(url, source, owner, tags, names):
            simplewebapp.formatResponse(format, self, "OK")
        else:
            simplewebapp.formatResponse(format, self, "FAILED")
    
    def post(self, format="json"):
        self.executeSave(format)
            
    def get(self, format="json"):
        self.executeSave(format)