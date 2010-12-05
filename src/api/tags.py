'''
Created on Oct 12, 2010

@author: outbounder
'''
import simplewebapp
from google.appengine.ext import webapp
from model import getTags

def getTagsNamedTree(parent=None):
    node = {'name':'root','nodes':[]};
    if parent != None:
        node['name'] = parent.name
    t = getTags(parent)
    for i in t:
        ir = getTagsNamedTree(i)
        node['nodes'].append(ir)
    return node

class Tags(webapp.RequestHandler):
    def get(self,format='json'):
        simplewebapp.formatResponse(format, self, getTagsNamedTree())