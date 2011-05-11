'''
Created on May 11, 2011

@author: outbounder
'''
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplewebapp

from model import Tag
from model import saveTag
from model import Entry
from model import getTagKeys
from rest.Urllib2Adapter import Resource
import simplejson
from simplejson.decoder import JSONDecoder
from model.Owner import Owner
resource = Resource()

class SynchTags(webapp.RequestHandler):
    
    def get(self,format):
        url = self.request.get("url").lower()
        try:
            content = resource.get(url).decodeBody().lower()
        except:
            content = ""
        
        tags = JSONDecoder().decode(content);
        
        ''' appends only new tags ''' 
        newTags = []
        for tag in tags:
            t = None
            t = Tag.all().filter("name = ", tag).fetch(1)
            if len(t) == 0:
                newTag = saveTag(tag, None);
                newTags.append(newTag.name)
        
        simplewebapp.formatResponse(format, self, newTags)