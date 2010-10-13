'''
Created on Oct 12, 2010

@author: outbounder
'''

import simplerestclient
from beautifulsoup.BeautifulSoup import BeautifulSoup
from model import Tag
from model import getAllTags



def getTags(url):
    content = simplerestclient.get(url)['content'].lower()
    soup = BeautifulSoup(content)
    
    resultedTags = []
    tags = getAllTags()
    for tag in tags:
        if soup.find(text=tag.name):
            resultedTags.append(tag.name)
            
    return resultedTags