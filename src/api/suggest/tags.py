'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp
import re
from beautifulsoup.BeautifulSoup import BeautifulSoup
from model import Tag
from model import Entry
from rest.Urllib2Adapter import Resource
resource = Resource()

def getTagsProposalsForText(text):
    result = []
    tags = Tag.all()
    for tag in tags:
        if re.search(r'\b'+re.escape(tag.name)+r'\b',text):
            result.append(tag.name)
        
    return result

def getTagsForUrl(url):
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
    visibleText = " ".join(visible_texts)
    
    result = getTagsProposalsForText(visibleText)
    
    entry = Entry.all().filter("url =", url).fetch(1)
    if len(entry) > 0:
        entryStableTags = entry[0].tags
        for t in entryStableTags:
            found = False
            name = Tag.get(t).name
            for r in result:
                if name == r:
                    found = True
            if not found:
                result.append(name)
                
    return result


class Tags(webapp.RequestHandler):
    def get(self,format="json"):
        url = self.request.get('url')
        
        if url.find("http://") != -1 or url.find("https://") != -1:
            simplewebapp.formatResponse(format, self, getTagsForUrl(url))
        else:
            simplewebapp.formatResponse(format, self, "FAILED")