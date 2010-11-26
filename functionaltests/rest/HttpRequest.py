from io import open
import Cookie

class HttpRequest(object):
    '''
    TODO
    '''


    def __init__(self, url, method = "", response = None, headers = [], body = [], files = []):
        '''
        Constructor
        '''
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.files = files
        self.cookies = []
        self.response = response
        
    def addHeader(self,name,value):
        self.header.append({'name':name,'value':value})
        return self
        
    def addCookie(self,name,value):
        self.cookies.append(Cookie(name,value))
        return self
        
    def addCookieObj(self,cookie):
        self.coockies.append(cookie)
        return self
        
    def addParams(self,params):
        self.body = params
        return self
        
    def addParam(self,paramName,paramValue):
        self.body.append({'param':paramName,'value':paramValue})
        return self
        
    def addFilepath(self, paramName, filepath):
        # self.addHeader('Transfer-Encoding','chunked') ?
        self.files.append({'file':open(filepath),'param':paramName})
        return self
        
    def addBinaryData(self,paramName, binaryData):
        self.addHeader('Transfer-Encoding','chunked')
        self.body.append({'param':paramName,'value':binaryData})
        return self