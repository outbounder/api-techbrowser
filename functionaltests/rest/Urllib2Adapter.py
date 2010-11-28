'''
howto use gathered from:
http://www.voidspace.org.uk/python/articles/urllib2.shtml
http://docs.python.org/release/2.5.2/lib/module-urllib2.html
http://docs.python.org/library/urllib2.html#urllib2.urlopen
'''

import urllib2

from api.REST import HttpResource
from api.HttpResponse import BaseHttpResponse

class ResourceAdapter(object):

    def send(self,request):
        response = BaseHttpResponse(request)
        
        try:
            if request.auth != None:
                if request.auth.type == "basic":
                    auth_handler = urllib2.HTTPBasicAuthHandler()
                    auth_handler.add_password(user=request.auth.username,
                                              passwd=request.auth.password)
                    opener = urllib2.build_opener(auth_handler)
                    if request.method != 'POST' and request.method != 'PUT':
                        r = opener.open(urllib2.Request(request.url, None, request.headers))  #, origin_req_host, unverifiable
                    else:
                        r = opener.open(urllib2.Request(request.url, request.dataParams, request.headers))  #, origin_req_host, unverifiable
                else:
                    raise TypeError('unsupported authType, possbile values: [basic]')
            else:
                if request.method != 'POST' and request.method != 'PUT':
                    r = urllib2.urlopen(urllib2.Request(request.url, None, request.headers))  #, origin_req_host, unverifiable
                else:
                    r = urllib2.urlopen(urllib2.Request(request.url, request.dataParams, request.headers))  #, origin_req_host, unverifiable
        except IOError, e:
            if hasattr(e, 'reason'):
                raise e
            elif hasattr(e, 'code'):
                response.status = e.code
                response.body = e.msg
                response.url = e.filename
        else:
            response.body = r.read()
            response.headers = r.info()
            response.url = r.geturl() 
            response.status = r.code
            
        return response 
    
class Resource(HttpResource):
    def __init__(self,endpoint=''):
        super(Resource, self).__init__(endpoint,ResourceAdapter())