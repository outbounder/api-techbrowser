import urllib2

class Urllib2Adapter(object):
    '''
    TODO
    '''


    def __init__(self,params):
        '''
        Constructor
        '''
    
    def send(self,request):
        # bellow is the code from current restful which needs rewrite to work with HttpRequest object     
        
        """
        Modified. Filename represents the actual file object.
        """
        params = None
        path = resource
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'restful_lib.py/' + __version__
            # add httplib2 info # + ' httplib2.py/' + version 
        
        BOUNDARY = u'00hoYUXOnLD5RQ8SKGYVgLLt64jejnMwtO7q8XE1'
        CRLF = u'\r\n'
        
        if filename:
            #fn = open(filename ,'r')
            #chunks = fn.read()
            #fn.close()
            
            content_type = self.get_content_type(filename.name)
            # Attempt to find the Mimetype
            headers['Content-Type']='multipart/form-data; boundary='+BOUNDARY

            encode_string = StringIO()

            if args:
              for key, val in args.items():
                encode_string.write(u'--' + BOUNDARY + CRLF)
                encode_string.write(u'Content-Disposition: form-data; name="%s"' % (key))
                encode_string.write(CRLF)
                encode_string.write(CRLF)
                encode_string.write(val)
                encode_string.write(CRLF)

            #encode_string.write(CRLF)
            encode_string.write(u'--' + BOUNDARY + CRLF)
            encode_string.write(u'Content-Disposition: form-data; name="file"; filename="%s"' % filename.name)
            encode_string.write(CRLF)
            encode_string.write(u'Content-Type: %s' % content_type + CRLF)
            encode_string.write(CRLF)
            encode_string.write(filename.read())
            encode_string.write(CRLF)
            encode_string.write(u'--' + BOUNDARY + u'--' + CRLF)

            filename.close()
            
            body = encode_string.getvalue()
            headers['Content-Length'] = str(len(body))
        elif body:
            if 'Content-Type' not in headers:
                headers['Content-Type']='text/xml'
            headers['Content-Length'] = str(len(body))        
        else:
            if 'Content-Length' in headers:
                del headers['Content-Length']
            
            headers['Content-Type']='text/plain'
            
            if args:
                if method == "get":
                    path += u"?" + urllib.urlencode(args)
                elif method == "put" or method == "post":
                    headers['Content-Type']='application/x-www-form-urlencoded'
                    body = urllib.urlencode(args)

            
        request_path = []
        # Normalise the / in the url path
        if self.path != "/":
            if self.path.endswith('/'):
                request_path.append(self.path[:-1])
            else:
                request_path.append(self.path)
            if path.startswith('/'):
                request_path.append(path[1:])
            else:
                request_path.append(path)
        
        resp, content = self.h.request(u"%s://%s%s" % (self.scheme, self.host, u'/'.join(request_path)), method.upper(), body=body, headers=headers )
        # TODO trust the return encoding type in the decode?
        return {u'headers':resp, u'body':content.decode('UTF-8')}