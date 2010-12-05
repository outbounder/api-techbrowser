'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplewebapp

from model import Tag
from model import saveTag

class ResetTags(webapp.RequestHandler):
    
    def get(self,format):
        tags = Tag.all().run()
        db.delete(tags)
        
        firstLevelTags = [
            'framework',
            'tool',
            'wiki',
            'tutorial',
            'howto',
            'library',
            'service',
            'language']
        
        secondLevelTags = [
            "ActionScript",
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
            "Scheme",
            "haxe"
        ]
        
        for tag in firstLevelTags:
            t = Tag(name=tag.lower())
            t.put()
            for st in secondLevelTags:
                saveTag(st.lower(),None, t)
            
        simplewebapp.formatResponse(format, self, "OK")
        