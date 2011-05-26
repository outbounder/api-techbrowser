#!/usr/bin/env python

#Copyright 2009 Thunderhead Consulting
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import sys
import os
import zipfile

def create_app_yaml(app_name):
	f = open("app.yaml", "w")
	print >>f, """\
application: %s
version: 1
runtime: python
api_version: 1

handlers:
- url: /css
  static_dir: css

- url: /js
  static_dir: js

- url: /favicon.png
  static_files: images/favicon.png
  upload: images/favicon.png

- url: /images
  static_dir: images

- url: /robots.txt
  static_files: robots.txt
  upload: robots.txt

- url: /.*
  script: MVCEngine.py
    """ % app_name
	f.close()

def create_robots_txt():
	f = open("robots.txt", "w")
	print >>f, """\
User-Agent: *
Allow: /
    """
	f.close()

def create_settings_py():
	f = open("settings.py", "w")
	print >>f, ""
	f.close()
	
def create_app_py():
	f = open("app/app.py", "w")
	print >>f, """\
from MVCEngine import MVCContext

class app(object):
    def routes(self, router):
        # The application should have all of its routes defined here.
        router.connect('', controller="home", action="index")
        router.connect('/:controller/:action/:id')
        router.connect('/:controller/:action')

    def load(self, context):
        # Put here any code that should be run every time
        # that your application handles a request
        pass

	def missing_controller(self, context):
        # This method is run when MVCEngine can not find a controller that has been requested.
        # If it returns an ActionResult, that ActionResult will be rendered as normal.
		pass

    def missing_action(self, context):
        # This method is run when MVCEngine can not find the requested action in the
        # requested controller. If it returns an ActionResult, that result will be rendered
        # as normal.
		pass
    """
	f.close()

def make_app_dir(path_elements):
	if type(path_elements) is str:
		os.mkdir(os.path.join(os.curdir, path_elements))
	else:
		os.mkdir(os.path.join(os.curdir, *path_elements))

def make_app_file(path_elements, file_contents=""):
	file_path = os.path.join(os.curdir, *path_elements)
	f = open(file_path, "w")
	print >>f, file_contents
	f.close()
	
def zipFileLocation():
	return os.path.join(os.path.dirname(__file__), "MVCFiles.zip")

def extractMVCLibFiles():
	mvcFiles = zipfile.ZipFile(zipFileLocation())
	for each_info in mvcFiles.infolist():
		if each_info.filename.startswith("gaemvclib/"):
			unzip_file = open(each_info.filename, "wb") # Need binary to prevent extra EOLs
			unzip_file.write(mvcFiles.read(each_info.filename))
			unzip_file.close()

def extractFromMVCFiles(to_extract):
	mvcFilesZip = zipfile.ZipFile(zipFileLocation())
	if type(to_extract) is str:
		to_extract = [to_extract]
		
	for each_info in mvcFilesZip.infolist():
		if each_info.filename in to_extract:
			unzip_file = open(each_info.filename, "wb") # Need binary to prevent extra EOLs
			unzip_file.write(mvcFilesZip.read(each_info.filename))
			unzip_file.close()
			
def extractMVCEngine():
	extractFromMVCFiles("MVCEngine.py")
	
def create_app(app_name):
	print "Creating application %s" % app_name
	make_app_dir(('app',))
	make_app_dir(('app','common'))
	make_app_dir(('app','controllers'))
	make_app_dir(('app','models'))
	make_app_dir(('app','tags'))
	make_app_file(('app','tags', '__init__.py'))
	make_app_dir(('app','views'))
	make_app_dir(('app','views','shared'))
	make_app_dir(('css',))
	make_app_dir(('images',))
	make_app_dir(('js',))
	make_app_dir(('gaemvclib',))
	make_app_file(('gaemvclib','__init__.py'))

	extractMVCLibFiles()
	extractMVCEngine()
	create_app_yaml(app_name)
	create_robots_txt()
	create_app_py()
	create_settings_py()
	add_controller("home")
	print "Finished creating application"

def add_controller(controller_name):
	print "Creating controller %s" % controller_name
	controller_filename = os.path.join(os.getcwd(),'app','controllers',"%s_controller.py" % controller_name)
	if not os.path.exists(controller_filename):
		f = open(controller_filename, "w")
		print >>f, """\
from MVCEngine import Controller

class %s_controller(Controller):
""" % controller_name

		print >>f, "\tpass"

		f.close()
	else:
		print "Controller already exists."
		
	view_path = os.path.join(os.getcwd(),'app','views', controller_name)
	if not os.path.exists(view_path):
		os.mkdir(view_path)

	print "Finished creating controller"

def requiresMVCFiles():
	if not os.path.exists(zipFileLocation()):
		print "This command requires that the file MVCFiles.zip be located in the"
		print "same directory as MVCTools.py"
		exit()

def main():
	command = ""
	if len(sys.argv) > 1:
		command = sys.argv[1]
		if len(sys.argv) > 2:
			params = sys.argv[2:]

	if command == "create_app":
		requiresMVCFiles()
		create_app(params[0])
	elif command == "add_controller":
		controller_name = params[0]
		add_controller(controller_name)
	else:
		print """Available commands:
create_app appname
add_controller controllername"""

if __name__ == "__main__":
	main()