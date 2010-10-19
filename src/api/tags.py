'''
Created on Oct 12, 2010

@author: outbounder
'''
import simplewebapp
from google.appengine.ext import webapp
from model import Tag

class Tags(webapp.RequestHandler):
    def get(self,format='json'):
        tags = Tag.all().run()
        
        tagNames = []
        for tag in tags:
            tagNames.append(tag.name)
            
        simplewebapp.formatResponse(format, self, tagNames)