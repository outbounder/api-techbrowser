'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplewebapp

from model import Tag

class ResetTags(webapp.RequestHandler):
    
    def get(self,format):
        tags = Tag.all().run()
        db.delete(tags)
        
        tagNames = ["ruby","javascript","grails","python","java","csharp","nodejs","rails","php","ajax","framework",
                    "mysql","couchdb","memcached","nosql","neo4j","groovy","mvc"]
        
        for tag in tagNames:
            t = Tag(name=tag)
            t.put()
            
        simplewebapp.formatResponse(format, self, "OK")
        