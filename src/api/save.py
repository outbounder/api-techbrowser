'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp

from model import saveTag

class SaveEntry(webapp.RequestHandler):
    def post(self,format="json"):
        # send the entry to external datastore via databroker unit
        # check if any of given tags are unknown (not stored in local datastore)
            # check if the unknown tag has been inputed more than 2 times
                # store the unknown tag to the local datastore
            # else
                # record the unkown tag proposal (increase its proposal value) and store in local memcached(?)
        simplewebapp.formatResponse(format,self,"NIY")
        
class SaveTag(webapp.RequestHandler):
    def post(self,format="json"):
        tagname = self.request.get("name")
        if saveTag(tagname):
            simplewebapp.formatResponse(format,self,"OK")
        else:
            simplewebapp.formatResponse(format,self,"FAILED")