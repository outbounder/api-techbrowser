import urllib
import array 

from HttpRequest import BaseHttpRequest

class HttpResource(object):
    def __init__(self, endpoint, http):
        self.endpoint = endpoint
        self.http = http
        
    def getDataParamsFromValue(self,value):
        '''
        convert value to dataParams dict collection
        value can be string('name1=value1&something=anotherthing') or array['name1=value1','name2=value2']
        '''
        dataParams = value
        
        if type(value) == str:
            dataParams = {}
            parts = value.split("&")
            for p in parts:
                pair = p.split("=")
                dataParams[pair[0]] = pair[1]
        elif type(value) == array:
            dataParams = {}
            for p in value:
                pair = p.split("=")
                dataParams[pair[0]] = pair[1]
                
        return dataParams
        
    def send(self,request):
        
        '''prepend endpoint if url does not specifies protocol schema'''
        if request.url.find("http://") != 0:
            request.url = self.endpoint+request.url
            
        ''' auto encode dataParams just before sending and append them to the URL '''
        if request.method != 'POST' and request.method != 'PUT':
            if len(request.dataParams.items()) > 0:
                if request.url.find("?") == -1:
                    request.url = request.url+"?"+urllib.urlencode(request.dataParams)
                else:
                    request.url += "&"+urllib.urlencode(request.dataParams)
        else:
            request.dataParams = urllib.urlencode(request.dataParams)
        
        return self.http.send(request)
    
    def get(self,url,data={}):
        return self.send(BaseHttpRequest(self,"GET",url,self.getDataParamsFromValue(data)))
    
    def post(self,url,data):
        return self.send(BaseHttpRequest(self,"POST",url,self.getDataParamsFromValue(data)))
    
    def delete(self,url,data={}):
        return self.send(BaseHttpRequest(self,"DELETE",url,self.getDataParamsFromValue(data)))
    
    def put(self,url,data):
        return self.send(BaseHttpRequest(self,"PUT",url,self.getDataParamsFromValue(data)))
    
    def head(self,url,data={}):
        return self.send(BaseHttpRequest(self,"HEAD",url,self.getDataParamsFromValue(data)))