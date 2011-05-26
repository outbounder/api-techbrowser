'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp

from libs import simplewebapp
from model import Tag

class Tags(webapp.RequestHandler):
    def get(self,format="json"):
        
        url = self.request.get('url')
        if url.find("http://") != -1 or url.find("https://") != -1:
            simplewebapp.formatResponse(format, self, Tag.getTagsForUrl(url))
        else:
            simplewebapp.formatResponse(format, self, "FAILED")
