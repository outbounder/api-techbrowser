class BaseHttpResponse(object):
    def __init__(self,request,url='',status=0,headers={},body=''):
        self.request = request
        self.url = url
        self.headers = headers
        self.body = body
        self.status = status
        
    def decodeBody(self,charset=None):
        ''' automatic decode of the content charset based on Content-Type header, ie text/html; charset="utf-8 '''
        if 'content-type' in self.headers and not charset:
            for param in self.headers['content-type'].split(';')[1:]:
                if param.strip().startswith('charset='):
                    charset = param.strip()[8:]
                    break
                
        if charset:
            return self.body.decode(charset, 'ignore')
        else:
            return self.body