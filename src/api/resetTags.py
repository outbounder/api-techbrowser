'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplewebapp

from model import Tag
from model import saveTag
from model import Entry
from model import getTagKeys

class ResetTags(webapp.RequestHandler):
    
    def get(self,format):
        tags = Tag.all().run()
        db.delete(tags)
        
        firstLevelTags = [
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
            "haxe",
            "nodejs",
            'framework',
            'tool',
            'wiki',
            'tutorial',
            'howto',
            'library',
            'service',
            'language'
        ]
        
        for tag in firstLevelTags:
            t = Tag(name=tag.lower())
            t.put()
            
        entries = Entry.all()
        for e in entries:
            newtags = getTagKeys(e.tagsRaw)
            e.tags = newtags
            e.put()
            
        simplewebapp.formatResponse(format, self, "OK")
        