'''
Created on Oct 12, 2010

@author: outbounder
'''
import simplewebapp
from google.appengine.ext import webapp
from model import Tag
from model import NameTag

class Tags(webapp.RequestHandler):
    def get(self,format='json'):
        tagNames = []
        
        
        tags = []
        t = Tag.all().run()
        for tag in t:
            tags.append(tag.name)
            
        n = NameTag.all().run()
        names = []
        for tag in n:
            names.append(tag.name)
            
        simplewebapp.formatResponse(format, self, {'tags': tags, 'names': names})