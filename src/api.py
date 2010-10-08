import bobo
import webob
import re

from simplejson import JSONEncoder


valid_callback = re.compile('^\w+(\.\w+)*$') 

def wrapToJSONP(json,callback):
    if callback and valid_callback.match(callback):
        json = '%s(%s)' % (callback, json)
            
    return json

@bobo.resource('/','GET','text/javascript')
def search(request):
    json = JSONEncoder().encode([{'url':'http://grails.org','name':'grails'},
                               {'url':'http://nodejs.org','name':'nodejs'}])
        
    return wrapToJSONP(json,request.params.get('callback',''))
        
@bobo.resource('/','POST','application/json')        
def save(request,callback=None):
    return wrapToJSONP(JSONEncoder().encode('NIY'), callback)
        
@bobo.resource('/suggest/search','GET','application/json')
def suggestSearch(request,callback=None):
    return wrapToJSONP(JSONEncoder().encode(['grails','nodejs']), callback)

@bobo.resource('/suggest/field','GET','application/json')
def suggestFieldName(request,callback=None):
    return wrapToJSONP(JSONEncoder().encode(['url','name']), callback)

@bobo.resource('/suggest/field/:field','GET','application/json')
def suggestFieldValue(request,field,callback=None):
    if field == "name":
        json = JSONEncoder().encode(['grails','nodejs'])
    elif field == "url":
        json = JSONEncoder().encode(['http://grails.org','http://nodejs.org'])
    else:
        json = JSONEncoder().encode([''])
        
    return wrapToJSONP(json, callback)