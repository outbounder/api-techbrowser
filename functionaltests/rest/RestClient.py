class RestClient(object):
    '''
    TODO
    '''


    def __init__(self,httpConnection):
        '''
        Constructor
        '''
        self.connection = httpConnection
        
    def send(self,request):
        '''
        returns HttpResponse
        '''
        return self.connection.send(request)
        