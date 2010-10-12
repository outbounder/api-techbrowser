'''
Created on Oct 12, 2010

@author: outbounder
'''
import simplewebapp
from google.appengine.ext import webapp
from model import getAllTags

class Tags(webapp.RequestHandler):
    def get(self,format='json'):
        tags = getAllTags()
        
        tagNames = []
        for tag in tags:
            tagNames.append(tag.name)
            
        simplewebapp.formatResponse(format, self, tagNames)