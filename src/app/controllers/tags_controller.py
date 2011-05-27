from app.common.restcontroller import RestController, RenderResponse
from app.models.Tag import Tag
from simplejson.decoder import JSONDecoder
from libs.restclient.Urllib2Adapter import Resource
from app.models.TagMismatch import TagMismatch

class tags_controller(RestController):
    
    def dump(self):
        result = []
        tags = Tag.all()
        for i in tags:
            result.append(i.name)
        return RenderResponse(self.context, result)
    
    def pull(self,url):
        url = url.lower()
        try:
            content = Resource().get(url).decodeBody().lower()
        except:
            content = ""
        
        tags = JSONDecoder().decode(content);
        
        ''' appends only new tags ''' 
        newTags = []
        for tag in tags:
            t = None
            t = Tag.all().filter("name = ", tag).fetch(1)
            if len(t) == 0:
                newTag = Tag.create(tag);
                newTags.append(newTag.name)
        
        return RenderResponse(self.context, newTags)

    def mismatch(self, tagname, tags):
        tagname = tagname.lower()
        tags = tags.split(" ")
        
        if TagMismatch.create(tagname, tags):
            RenderResponse(self.context,  "OK")
        else:
            RenderResponse(self.context,  "FAILED")
            
    def related(self, tags):
        results = []
        
        tagsRaw = tags.lower().split(" ")
        
        if len(tagsRaw) == 0 or tagsRaw[0] == "": 
            return RenderResponse(self.context, results)
        
        results = Tag.findRelatedTags(tagsRaw) 

        return RenderResponse(self.context, results)
    
    def suggest(self,url):
        if url.find("http://") != -1 or url.find("https://") != -1:
            return RenderResponse(self.context, Tag.getTagsForUrl(url))
        else:
            return RenderResponse(self.context, "FAILED")
    
    def query(self,q):
        query = q.lower()
        if len(query) == 0:
            RenderResponse(self.context,[])
            return
        
        return RenderResponse(self.context, Tag.listStartingWith(query))
        
    def create(self):
        return RenderResponse(self.context)    
