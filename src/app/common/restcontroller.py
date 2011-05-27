import re
from MVCEngine import Controller
from MVCEngine import RenderString
from simplejson import JSONEncoder
from libs.obj2xml import Object2Xml

obj2xml = Object2Xml(None, None)

valid_callback = re.compile('^\w+(\.\w+)*$')
XML_CONTENT_TYPE = "application/xml"
JSON_CONTENT_TYPE = "application/json"
PLAIN_CONTENT_TYPE = "text/javascript"
JSONP_CALLBACKNAME = "callback"

from mimetypes import MimeTypes
mimetypes = MimeTypes()
mimetypes.add_type("application/json", ".json")

class RestController(Controller):
    
    def index(self,id):
        if id == None:
            return RenderString(self.context, "actions: index,query,post,put,delete")
        else:
            return RenderString(self.context, "id: "+id)

class RenderResponse(RenderString):
    def __init__(self, context, content):
        super(RenderString, self).__init__(context)
        self.content = content

    def Render(self):
        self.writeResponse(self.getRenderFormat(), self.content)
        
    def getRenderFormat(self):
        out_mime_type = self.context.request.accept.best_match([JSON_CONTENT_TYPE, XML_CONTENT_TYPE])
        if(out_mime_type == JSON_CONTENT_TYPE or mimetypes.guess_type(self.context.request.url)[0]==JSON_CONTENT_TYPE):
            return "json"
        elif(out_mime_type == XML_CONTENT_TYPE or mimetypes.guess_type(self.context.request.url)[0]==XML_CONTENT_TYPE):
            return "xml"
        return None
    
    def writeResponse(self,format,data):
        if format == "json":
            self.writeResponseAsJSON(data)
        elif format == "xml":
            self.writeResponseAsXML(data)
        else:
            self.context.response.out.write(data)
            
    def writeResponseAsJSON(self,data):
        callback = self.context.request.get(JSONP_CALLBACKNAME)
        if not callback:
            self.context.response.headers["Content-Type"] = JSON_CONTENT_TYPE
            self.context.response.out.write(JSONEncoder().encode(data))
        else:
            self.context.response.headers["Content-Type"] = PLAIN_CONTENT_TYPE
            json = JSONEncoder().encode(data)
            if callback and valid_callback.match(callback):
                json = '%s(%s)' % (callback, json)
            self.context.response.out.write(json)
    
    def writeResponseAsXML(self,data):
        self.context.response.headers["Content-Type"] = XML_CONTENT_TYPE
        self.context.response.out.write(obj2xml.getXML({data: data},'object')) # FIXXX 
        