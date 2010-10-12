from google.appengine.ext import db

class Tag(db.Expando):
    name = db.StringProperty()
    
class SearchQuery(db.Expando):
    query = db.StringProperty()

def getAllTags():
    return Tag.all().run()

def saveTag(tagname):
    q = Tag.all()
    q.filter("name =", tagname)
    r = q.fetch(1)
    if len(r) == 0:
        t = Tag(name=tagname)
        t.put()
        return True
    else:
        return False
        
def getAllSearchQueries():
    return SearchQuery.all().run()
    
def getMockupSearchResults():
    return [{'url':'http://grails.org','name':'grails'},
     {'url':'http://nodejs.org','name':'nodejs'},
     {'url':'http://python.org','name':'python'},
     {'url':'http://rubyonrails.org','name':'rails'},
     {'url':'http://www.ruby-lang.org','name':'ruby'},
     {'url':'http://haxe.org/','name':'haxe'},
     {'url':'http://flex.org/','name':'flex'}]
    
def getMockupSearchQuerySuggestions():
    return ['grails','nodejs','python','rails','ruby','haxe','flex']