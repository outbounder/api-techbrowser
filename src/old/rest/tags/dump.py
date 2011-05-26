'''
Created on Oct 12, 2010

@author: outbounder
'''
from libs import simplewebapp
from google.appengine.ext import webapp
from model import Tag

def getTags():
    result = []
    tags = Tag.all()
    for i in tags:
        result.append(i.name)
    return result

class Tags(webapp.RequestHandler):
    def get(self,format='json'):
        simplewebapp.formatResponse(format, self, getTags())