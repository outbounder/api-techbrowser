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
        
        tagNames = [
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
        
        for tag in tagNames:
            t = Tag(name=tag.lower())
            t.put()
            
        simplewebapp.formatResponse(format, self, "OK")
        