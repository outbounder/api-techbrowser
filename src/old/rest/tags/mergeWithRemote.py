'''
Created on May 11, 2011

@author: outbounder
'''
from google.appengine.ext import webapp
from libs import simplewebapp

from model import Tag

from simplejson.decoder import JSONDecoder

from libs.rest.Urllib2Adapter import Resource

class MergeWithRemote(webapp.RequestHandler):
    
    def get(self,format): 
        url = self.request.get("url").lower()
        try:
            content = Resource().get(url).decodeBody().lower()
        except:
            content = ""
        
        tags = JSONDecoder().decode(content);
        
        ''' appends only new tags ''' 
        newTags = []
        for tag in tags:
            t = None
            t = Tag.all().filter("name = ", tag).fetch(1)
            if len(t) == 0:
                newTag = Tag.create(tag);
                newTags.append(newTag.name)
        
        simplewebapp.formatResponse(format, self, newTags)