'''
Created on Oct 19, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp
from model import deleteOwner

class DeleteOwner(webapp.RequestHandler):
    def post(self,ownerUID,format="json"):
        source = self.request.get("source")
        if len(ownerUID) == 0 or len(source) == 0:
            simplewebapp.formatResponse(format, self, "FAILED")
            return
        
        if deleteOwner(ownerUID,source):
            simplewebapp.formatResponse(format, self, "OK")
        else:
            simplewebapp.formatResponse(format, self, "FAILED")