from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from api.entries.save import SaveEntry
from api.entries.search import SearchEntries
from api.tags.search import SearchTags
from api.tags.get import Tags
from api.suggest.tags import Tags as TagsSuggest
from api.suggest.tag import Tag as TagSuggest
from api.tags.synch import SynchTags
from api.tags.recordMismatch import RecordMismatch


application = webapp.WSGIApplication([
                                      ('/entry\.(.*)', SaveEntry),
                                      ('/tags\.(.*)', Tags),
                                      ('/search\.(.*)', SearchEntries),
                                      ('/searchTags\.(.*)', SearchTags),
                                      ('/suggest/tags\.(.*)', TagsSuggest),
                                      ('/suggest/tag\.(.*)', TagSuggest),
                                      ('/synchTags\.(.*)', SynchTags),
                                      ('/recordTagMismatch\.(.*)', RecordMismatch)
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()