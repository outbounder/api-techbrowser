import httplib2

from api.REST import HttpResource
from api.HttpResponse import BaseHttpResponse

class ResourceAdapter(object):

    def send(self,request):
        
        response = BaseHttpResponse(request)
        
        conn = httplib2.Http(".cache") # timeout ?
        
        if request.auth != None:
            if request.auth.type == "basic":
                conn.add_credentials(request.auth.username, request.auth.password)
            else:
                raise TypeError('unsupported authType, possbile values: [basic]')
        try:    
            r,c = conn.request(request.url, request.method, headers=request.headers, body=request.dataParams)
        except Exception, e:
            raise IOError("could not connect to "+request.url) # improve
        else:
            response.body = c
            response.headers = r
            response.url = request.url # with httplib2 how to get final url (after http forwards)?
            response.status = r['status']
            
        return response 
    
class Resource(HttpResource):
    def __init__(self,endpoint=''):
        super(Resource, self).__init__(endpoint,ResourceAdapter())