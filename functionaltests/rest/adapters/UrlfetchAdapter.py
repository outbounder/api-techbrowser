from google.appengine.api import urlfetch

class UrlfetchAdapter(object):
    '''
    TODO
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
    def send(self,request):
        # bellow is a code from the simpliest usa case of urlfetch. needs extending to support HttpRequest object
        
        urlfetch_response = urlfetch.fetch(url, method=method, payload=args, headers=headers)
        r_headers={'status':urlfetch_response.status_code}
        
        for header_key in urlfetch_response.headers:
            r_headers[header_key.lower()] = urlfetch_response.headers[header_key]
            
        content = urlfetch_response.content