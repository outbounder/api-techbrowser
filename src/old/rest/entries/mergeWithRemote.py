'''
Created on May 11, 2011

@author: outbounder
'''
from google.appengine.ext import webapp
from libs import simplewebapp

from model import Entry

from simplejson.decoder import JSONDecoder

from libs.rest.Urllib2Adapter import Resource

class MergeWithRemote(webapp.RequestHandler):
    
    def get(self,format):
        url = self.request.get("url").lower()
        try:
            content = Resource().get(url).decodeBody().lower()
        except:
            content = ""
        
        entries = JSONDecoder().decode(content);
        
        ''' appends only new tags if they do not exist in db ''' 
        newEntries = []
        for entry in entries:
            t = None
            t = Entry.all().filter("url = ", entry.url).fetch(1)
            if len(t) == 0:
                newEntry = Entry.create(entry.url, entry.tagsRaw);
                newEntries.append(newEntry.name)
        
        simplewebapp.formatResponse(format, self, newEntries)