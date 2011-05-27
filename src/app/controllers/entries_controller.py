from app.common.restcontroller import RestController, RenderResponse
from app.models.Entry import Entry

from simplejson.decoder import JSONDecoder

from libs.restclient.Urllib2Adapter import Resource

class entries_controller(RestController):
    
    def dump(self):
        result = []
        entries = Entry.all()
        for i in entries:
            result.append({'url':i.url, 'tagsRaw': i.tagsRaw})
        return RenderResponse(self.context, result)
    
    def pull(self, url):
        url = self.request.get("url").lower()
        try:
            content = Resource().get(url).decodeBody().lower()
        except:
            content = ""
        
        entries = JSONDecoder().decode(content);
        
        ''' appends only new tags if they do not exist in db ''' 
        newEntries = []
        for entry in entries:
            t = None
            t = Entry.all().filter("url = ", entry.url).fetch(1)
            if len(t) == 0:
                newEntry = Entry.create(entry.url, entry.tagsRaw);
                newEntries.append(newEntry.name)
        
        return RenderResponse(self.context, newEntries)
    
    def query(self, tags):
        results = []
        
        tagsRaw = tags.lower().split(" ")
        
        if len(tagsRaw) == 0 or tagsRaw[0] == "": 
            return RenderResponse(self.context, results)
        
        # EXTREMELY SLOW ! OPTIMIZE!
        results = Entry.matchByTags(tagsRaw)
                
        return RenderResponse(self.context, results)
    
    def submit(self, url, tags):
        url = url.lower()
        if url.find("http://") == -1 and url.find("https://") == -1:
            return RenderResponse(self.context, "FAILED")
        
        tags = tags.lower().split(" ")
        if Entry.create(url, tags): 
            return RenderResponse(self.context, "OK")
        else:
            return RenderResponse(self.context, "FAILED")
        
    
        
