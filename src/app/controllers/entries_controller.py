from MVCEngine import Controller
from MVCEngine import RenderString
from MVCEngine import HttpVerbs

class entries_controller(Controller):
    
    def index(self,id):
        if id == None:
            return RenderString(self.context, "actions: index,query,post,put,delete")
        else:
            return RenderString(self.context, "id: "+id)
    
    @Controller.respond_to(HttpVerbs.GET)
    def query(self, q):
        return RenderString(self.context, "entry with "+q)
