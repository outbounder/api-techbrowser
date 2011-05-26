'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
from libs import simplewebapp

from model.Entry import Entry

class Save(webapp.RequestHandler):
    def executeSave(self, format):
        url = self.request.get("url").lower()
        if url.find("http://") == -1 and url.find("https://") == -1:
            simplewebapp.formatResponse(format, self, "FAILED")
            return
        
        tags = self.request.get("tags").lower().split(" ")
        if Entry.create(url, tags):
            simplewebapp.formatResponse(format, self, "OK")
        else:
            simplewebapp.formatResponse(format, self, "FAILED")
    
    def post(self, format="json"):
        self.executeSave(format)
            
    def get(self, format="json"):
        self.executeSave(format)