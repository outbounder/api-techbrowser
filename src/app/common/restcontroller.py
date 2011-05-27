import re
from MVCEngine import Controller
from MVCEngine import RenderString
from simplejson import JSONEncoder
from numbers import Number

valid_callback = re.compile('^\w+(\.\w+)*$')
XML_CONTENT_TYPE = "application/xml"
JSON_CONTENT_TYPE = "application/json"
PLAIN_CONTENT_TYPE = "text/javascript"
JSONP_CALLBACKNAME = "callback"

from mimetypes import MimeTypes
mimetypes = MimeTypes()
mimetypes.add_type("application/json", ".json")

class RestController(Controller):

    def index(self, id):
        if id == None:
            return RenderString(self.context, "actions: index,query,post,put,delete")
        else:
            return RenderString(self.context, "id: " + id)

class RenderResponse(RenderString):
    def __init__(self, context, content):
        super(RenderString, self).__init__(context)
        self.content = content

    def Render(self):
        self.writeResponse(self.getRenderFormat(), self.content)

    def getRenderFormat(self):
        out_mime_type = self.context.request.accept.best_match([JSON_CONTENT_TYPE, XML_CONTENT_TYPE])
        if(out_mime_type == JSON_CONTENT_TYPE or mimetypes.guess_type(self.context.request.path)[0] == JSON_CONTENT_TYPE):
            return "json"
        elif(out_mime_type == XML_CONTENT_TYPE or mimetypes.guess_type(self.context.request.path)[0] == XML_CONTENT_TYPE):
            return "xml"
        return None

    def writeResponse(self, format, data):
        if format == "json":
            self.writeResponseAsJSON(data)
        elif format == "xml":
            self.writeResponseAsXML(data)
        else:
            self.context.response.out.write(data)

    def writeResponseAsJSON(self, data):
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

    def writeResponseAsXML(self, data):
        self.context.response.headers["Content-Type"] = XML_CONTENT_TYPE
        if isinstance(data, str) or isinstance(data, Number):
            doc = "<object>" + data + "</object>"
            self.context.response.out.write(doc)
        else:
            doc = parse_doc(data)
            self.context.response.out.write(doc.toprettyxml(encoding="utf-8", indent="  ")) 

import sys
import json
import traceback
import getopt
import numbers

from xml.dom.minidom import Document

def parse_element(doc, root, j):
  if isinstance(j, dict):
    for key in j.keys():
      value = j[key]
      if isinstance(value, list):
        listRoot = doc.createElement(key)
        for e in value:
          elem = doc.createElement("object")
          parse_element(doc, elem, e)
          listRoot.appendChild(elem)
        root.appendChild(listRoot)
      else:
        if key.isdigit():
          elem = doc.createElement('object')
          elem.setAttribute('value', key)
        else:
          elem = doc.createElement(key)
        parse_element(doc, elem, value)
        root.appendChild(elem)
  elif isinstance(j, str) or isinstance(j, unicode):
    text = doc.createTextNode(j)
    root.appendChild(text)
  elif isinstance(j, numbers.Number):
    text = doc.createTextNode(str(j))
    root.appendChild(text)
  else:
    raise Exception("bad type '%s' for '%s'" % (type(j), j,))

def parse_doc(j):
  doc = Document()
  if isinstance(j,list):
    listRoot = doc.createElement("array")
    for e in j:
      elem = doc.createElement("object")
      parse_element(doc, elem, e)
      listRoot.appendChild(elem)
    doc.appendChild(listRoot)
  else:
    if len(j.keys()) > 1:
      raise Exception('Expected one root element, or use --root to set root')
    root = j.keys()[0]
    j = j[root]
    elem = doc.createElement(root)
    parse_element(doc, elem, j)
    doc.appendChild(elem)
  return doc

