from simplejson import JSONEncoder
import re

def formatResponseJSON(self,data):
    self.response.headers["Content-Type"] = "application/json"
    self.response.out.write(JSONEncoder().encode(data))
    
valid_callback = re.compile('^\w+(\.\w+)*$')     
def formatResponseJSONP(self,data,callbackName='callback'):
    self.response.headers["Content-Type"] = "text/javascript"
    callback = self.request.get(callbackName)
    json = JSONEncoder().encode(data)
    if callback and valid_callback.match(callback):
        json = '%s(%s)' % (callback, json)
    self.response.out.write(json)
    
def formatResponse(format,self,data):
    if format == "json":
        formatResponseJSON(self,data)
    elif format == "jsonp":
        formatResponseJSONP(self,data)
    else:
        self.response.out.write(data)