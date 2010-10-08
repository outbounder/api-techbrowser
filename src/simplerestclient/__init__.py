__license__ = 'MIT'
__author__ = "outbounder <obiwonn@gmail.com>"
__version__ = '0.1'

from google.appengine.api import urlfetch

def get(url,args=None,headers={}):
    return request(urlfetch.GET, url, args, headers)

def post(url,args=None,headers={}):
    return request(urlfetch.POST, url, args, headers)

def request(method,url,args=None,headers={},charset=None):
    
    urlfetch_response = urlfetch.fetch(url, method=method, payload=args, headers=headers)
    r_headers={'status':urlfetch_response.status_code}
    
    for header_key in urlfetch_response.headers:
        r_headers[header_key.lower()] = urlfetch_response.headers[header_key]
        
    content = urlfetch_response.content
    
    # automatic decode of the content based on Content-Type header, ie text/html; charset="utf-8
    if 'content-type' in r_headers and not charset:
        for param in r_headers['content-type'].split(';')[1:]:
            if param.strip().startswith('charset='):
                charset = param.strip()[8:]
                break
    if charset:
        content = content.decode(charset, 'ignore')
        
    return {'headers':r_headers, 'content':content}