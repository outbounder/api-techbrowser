'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp

class Own(webapp.RequestHandler):
    def get(self,format="json"):
        simplewebapp.formatResponse(format,self,[{'url':'http://grails.org','name':'grails'},
                               {'url':'http://nodejs.org','name':'nodejs'}])