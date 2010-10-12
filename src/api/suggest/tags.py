'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp
from autotags import genericAutoTagGenerator

class Tags(webapp.RequestHandler):
    def get(self,format="json"):
        url = self.request.get('url')
        simplewebapp.formatResponse(format, self, genericAutoTagGenerator.getTags(url))