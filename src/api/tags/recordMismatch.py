'''
Created on May 15, 2010

@author: outbounder
'''
import simplewebapp
from google.appengine.ext import webapp
from model import saveTagMismatch

class RecordMismatch(webapp.RequestHandler):
    def executeSave(self, format):
        tagname = self.request.get("tagname").lower()
        tags = self.request.get("tags").split(" ")
        
        owner = self.request.get("owner").lower()
        if saveTagMismatch(tagname, tags, owner):
            simplewebapp.formatResponse(format, self, "OK")
        else:
            simplewebapp.formatResponse(format, self, "FAILED")
    
    def post(self, format="json"):
        self.executeSave(format)
            
    def get(self, format="json"):
        self.executeSave(format)