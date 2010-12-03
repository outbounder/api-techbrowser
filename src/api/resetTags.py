'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplewebapp

from model import Tag
from model import NameTag

class ResetTags(webapp.RequestHandler):
    
    def get(self,format):
        tags = Tag.all().run()
        db.delete(tags)
        
        nameTags = NameTag.all().run()
        db.delete(nameTags)
        
        tags = [
            "ActionScript",
            "AppleScript",
            "Asp",
            "BASIC",
            "C",
            "C++",
            "Clojure",
            "COBOL",
            "ColdFusion",
            "Erlang",
            "Fortran",
            "Groovy",
            "Haskell",
            "Java",
            "JavaScript",
            "Lisp",
            "Perl",
            "PHP",
            "Python",
            "Ruby",
            "Scala",
            "Scheme"
        ]
        
        nameTags = [
            "blog",
            "wiki",
            "howto",
            "tutorial",
            "library",
            "tool",
            "service",
            "project",
            "language"
        ]
        
        for tag in tags:
            t = Tag(name=tag.lower())
            t.put()
            
        for tag in nameTags:
            t = NameTag(name=tag.lower())
            t.put()
            
        simplewebapp.formatResponse(format, self, "OK")
        