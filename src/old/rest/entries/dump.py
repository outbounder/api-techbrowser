'''
Created on Oct 12, 2010

@author: outbounder
'''
from libs import simplewebapp
from google.appengine.ext import webapp
from model import Entry

def dumpEntries():
    result = []
    entries = Entry.all()
    for i in entries:
        result.append({'url':i.url, 'tagsRaw': i.tagsRaw})
    return result

class Tags(webapp.RequestHandler):
    def get(self,format='json'):
        simplewebapp.formatResponse(format, self, dumpEntries())