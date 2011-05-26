class BaseHttpAuthCredentials(object):
    def __init__(self, username,password,authType):
        self.username = username
        self.password = password
        self.authType = authType

class BaseHttpRequest(object):
    def __init__(self, resource, method = "", url = "", dataParams = {}, headers = {}, timeout = 60*3):
        self.resource = resource
        self.url = url
        self.method = method
        if not 'User-Agent' in headers:
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.50 Safari/534.24"
        if not 'Accept' in headers:
            headers['Accept'] = "application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"
        self.headers = headers
        self.dataParams = dataParams
        self.timeout = timeout
        self.auth = None
        
    def setAuth(self,username,password,authType):
        self.auth = BaseHttpAuthCredentials(username,password,authType)
        return self
        
    def setHeader(self,name,value):
        self.headers[name] = value
        return self
        
    def setDataParams(self,dataParams):
        self.dataParams = dataParams
        return self
        
    def addDataParam(self,paramName,paramValue):
        self.dataParams[paramName] = paramValue
        return self