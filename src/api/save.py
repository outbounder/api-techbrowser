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
        # TODO replace current impl. with:
        # send the entry to external datastore via databroker unit
        # check if any of given tags are unknown (not stored in local datastore)
            # check if the unknown tag has been inputed more than 2 times
                # store the unknown tag to the local datastore
            # else
                # record the unkown tag proposal (increase its proposal value) and store in local memcached(?)
        url = self.request.get("url").lower()
        if url.find("http://") == -1:
            simplewebapp.formatResponse(format, self, "FAILED")
            return
        
        tagsRaw = getTagTerms(self.request.get("tags").lower())
        owner = self.request.get("owner").lower()
        if saveEntry(url, owner, tagsRaw):
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

