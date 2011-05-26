'''
Created on May 15, 2010

@author: outbounder
'''
from libs import simplewebapp
from google.appengine.ext import webapp
from model.TagMismatch import TagMismatch

class RecordMismatch(webapp.RequestHandler):
    def executeSave(self, format):
        tagname = self.request.get("tagname").lower()
        tags = self.request.get("tags").split(" ")
        
        if TagMismatch.create(tagname, tags):
            simplewebapp.formatResponse(format, self, "OK")
        else:
            simplewebapp.formatResponse(format, self, "FAILED")
    
    def post(self, format="json"):
        self.executeSave(format)
            
    def get(self, format="json"):
        self.executeSave(format)