'''
Created on Oct 12, 2010

@author: outbounder
'''
from google.appengine.ext import webapp
import simplewebapp
import re
from beautifulsoup.BeautifulSoup import BeautifulSoup
from model import getTags
from rest.Urllib2Adapter import Resource
resource = Resource()

def getTagsProposalsForText(text,tagsParent):
    result = []
    hits = 0
    tags = getTags(tagsParent)
    for tag in tags:
        count = len(re.findall(r'\b'+re.escape(tag.name)+r'\b',text))
        if count > 0:
            children, childrenHits = getTagsProposalsForText(text, tag)
            result.append({'name': tag.name, 'childs': children, 'hits': count+childrenHits})
            hits += childrenHits;
        hits += count
        
    return result, hits

def convertProposalToTagsList(proposal):
    result = []
    result.append(proposal['name'])
    
    bestScore = 0
    bestProposal = None
    for i in proposal['childs']:
        if i['hits'] >= bestScore:
            bestScore = i['hits']
            bestProposal = i
    
    if bestProposal != None:    
        r = convertProposalToTagsList(bestProposal)
        for k in r:
            result.append(k)
            
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
    
    proposals, hits = getTagsProposalsForText(visibleText, None)
    if hits == 0:
        return []
    
    bestProposal = None
    bestProposalHitScore = 0
    for p in proposals:
        if p['hits'] >= bestProposalHitScore:
            bestProposal = p
            bestProposalHitScore = p['hits']
    
    if bestProposal == None:
        return []
    
    return convertProposalToTagsList(bestProposal)


class Tags(webapp.RequestHandler):
    def get(self,format="json"):
        url = self.request.get('url')
        
        if url.find("http://") != -1 or url.find("https://") != -1:
            simplewebapp.formatResponse(format, self, getTagsForUrl(url))
        else:
            simplewebapp.formatResponse(format, self, "FAILED")