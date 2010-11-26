import RestClient
import HttpRequest
import HttpResponse

from adapters.Urllib2Adapter import Urllib2Adapter


# fast methods using urllib2 adapter as default low level http protocol implementation 
restClient = RestClient(Urllib2Adapter())

def urlGET(url,params):
    return restClient.send(HttpRequest(url,"GET",HttpResponse()).addParams(params)).decodeBody()

def urlPOST(url,params):
    return restClient.send(HttpRequest(url,"POST",HttpResponse()).addParams(params)).decodeBody()

def urlUPLOAD(url,filepath,paramName,additionalParams=[]):
    return restClient.send(HttpRequest(url,"POST",HttpResponse()).addFilepath(paramName, filepath).addParams(additionalParams)).decodeBody()