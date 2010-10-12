from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from api.save import SaveEntry
from api.save import SaveTag
from api.search import Search
from api.own import Own
from api.suggest.search import Search as SearchSuggest
from api.suggest.tags import Tags as TagsSuggest
from api.suggest.tag import Tag as TagSuggest
from api.resetTags import ResetTags

application = webapp.WSGIApplication([('/entry.(.*)', SaveEntry),
                                      ('/tag.(.*)', SaveTag),
                                      ('/search.(.*)', Search),
                                      ('/own.(.*)', Own),
                                      ('/suggest/tags.(.*)', TagsSuggest),
                                      ('/suggest/search.(.*)', SearchSuggest),
                                      ('/suggest/tag.(.*)', TagSuggest),
                                      ('/resettags.(.*)', ResetTags)
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
