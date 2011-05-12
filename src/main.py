from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from api.save import SaveEntry
from api.search import Search
from api.search import SearchOwn
from api.tags import Tags
from api.suggest.tags import Tags as TagsSuggest
from api.suggest.tag import Tag as TagSuggest
from api.resetTags import ResetTags
from api.synchTags import SynchTags


application = webapp.WSGIApplication([('/entry\.(.*)', SaveEntry),
                                      ('/user/(.*)/search\.(.*)', SearchOwn),
                                      ('/tags\.(.*)', Tags),
                                      ('/search\.(.*)', Search),
                                      ('/suggest/tags\.(.*)', TagsSuggest),
                                      ('/suggest/tag\.(.*)', TagSuggest),
                                      ('/synchTags\.(.*)', SynchTags)
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()