import bobo

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


bobo_app_name='api'


def main():
    application = bobo.Application(bobo_resources=bobo_app_name)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
