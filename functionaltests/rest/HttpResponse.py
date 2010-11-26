import json

class HttpResponse(object):
    '''
    TODO
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.request = None
        self.headers = None
        self.body = None
        self.status = None
        
    def decodeBody(self,charset):
        # automatic decode of the content charset based on Content-Type header, ie text/html; charset="utf-8
        if 'content-type' in self.headers and not charset:
            for param in self.headers['content-type'].split(';')[1:]:
                if param.strip().startswith('charset='):
                    charset = param.strip()[8:]
                    break
                
        if charset:
            return self.body.decode(charset, 'ignore')
        else:
            return self.body
        
        
def JSONResponse(HttpResponse):
    
    def decodeBody(self,charset):
        return json.loads(super(JSONResponse, self).decodeBody(charset))