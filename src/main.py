from google.appengine.dist import use_library
use_library('django', '1.2') # need to be first, otherwise other libs include the wrong version

from google.appengine.ext.webapp.util import run_wsgi_app

from libs.MVCEngine.MVCEngine import MVCEngine 
from libs import restserver
from app.models.Entry import Entry
from app.models.Tag import Tag
from app.models.TagProposal import TagProposal
from app.models.TagMismatch import TagMismatch



restserver.Dispatcher.base_url = '/models'
restserver.Dispatcher.add_models({
  'entry' : Entry,
  'tag' : Tag,
  'tagProposal' : TagProposal,
  'tagMismatch' : TagMismatch})

application = MVCEngine.createApplication([('/models/.*', restserver.Dispatcher)])

def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()
