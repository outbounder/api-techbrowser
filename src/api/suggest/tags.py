'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp
import re
from beautifulsoup.BeautifulSoup import BeautifulSoup
from model import Tag
from rest.Urllib2Adapter import Resource
resource = Resource()

def getTags(url):
    try:
        content = resource.get(url).decodeBody().lower()
    except:
        content = ""
    
    soup = BeautifulSoup(content) 
    texts = soup.findAll(text=True)

    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True
    
    visible_texts = filter(visible, texts)
    
    resultedTags = []
    tags = Tag.all().run()
    for tag in tags:
        for t in visible_texts:
            if t.find(tag.name) != -1:
                resultedTags.append(tag.name)
                break
            
    return resultedTags

class Tags(webapp.RequestHandler):
    def get(self,format="json"):
        url = self.request.get('url')
        
        if url.find("http://") != -1 or url.find("https://") != -1:
            simplewebapp.formatResponse(format, self, getTags(url))
        else:
            simplewebapp.formatResponse(format, self, [])