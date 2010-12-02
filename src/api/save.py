'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp

from model import saveTag
from model import saveEntry
from model import getTagTerms 
from model import saveOwner

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
        
class SaveTag(webapp.RequestHandler):
    def post(self, format="json"):
        tagname = self.request.get("name")
        owner = self.request.get("owner")
        if saveTag(tagname, owner):
            simplewebapp.formatResponse(format, self, "OK")
        else:
            simplewebapp.formatResponse(format, self, "FAILED")
            
class SaveOwner(webapp.RequestHandler):
    def post(self, uid, format="json"):
        source = self.request.get("source")
        if saveOwner(uid, source):
            simplewebapp.formatResponse(format, self, "OK")
        else:
            simplewebapp.formatResponse(format, self, "FAILED")

