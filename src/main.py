from google.appengine.dist import use_library
import logging
import sys
use_library('django', '1.2') # need to be first, otherwise other libs include the wrong version

from google.appengine.ext.webapp.util import run_wsgi_app
from libs.MVCEngine.MVCEngine import MVCEngine 

application = MVCEngine.createApplication()

def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()
