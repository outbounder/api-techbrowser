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

import unittest
import urllib
import httplib
import os
import sys
import logging
from urlparse import urlparse

logging.getLogger().setLevel(logging.DEBUG)

def test_name():
    import __main__
    """Return the name of the test file that we are running. Used to determine
    the directory in which the test application runs."""
    return os.path.basename(__main__.__file__).replace(".py","").replace(".pyc","").replace("_tests","")

class AppServer(object):
    app_server_process = None
    app_server_port = 8080

    @staticmethod
    def __is_running(on_port):
        running = False
        try:
            connection = httplib.HTTPConnection('localhost', on_port)
            connection.request("GET", "/_ah/admin/datastore")
            response = connection.getresponse()
            if response.status == 200:
                running = True
        except:
            logging.info("Caught an exception while checking for dev_appserver.py running on port %d; assuming that server is not running." % on_port)

        return running

    @staticmethod
    def start(on_port = 8080):
        opened_successfully = False
            
        if not AppServer.__is_running(on_port):
            # The server is not running. Start it up.
            startup_command = "dev_appserver.py --port=%d %s/"  % (on_port, test_name())
            command_to_spawn = startup_command
            if os.name == "nt":
                # If running on Windows, we need to run the appserver in
                # a command shell to make sure that we have all of our
                # environment variables set up correctly.
                command_to_spawn = "cmd /K %s" % startup_command
            
            logging.info("Starting up appserver with command line:\n%s" % startup_command)

            try:
                import wexpect as pexpect
            except ImportError:
                # wexpect does not exist, so we may be running on Unix, try pexpect
                try:
                    import pexpect
                except ImportError:
                    # Couldn't find wexpect or pexpect; issue helpful information message.
                    logging.info("Could not find wexpect or pexpect; unable to start server.")
                    logging.info("Most tests may fail; start server manually and re-run tests.")
                    if os.name == "nt":
                        logging.info("Please consider installing wexpect: http://www.wstein.org/home/goreckc/sage/wexpect")
                    else:
                        logging.info("Please consider installing pexpect: http://sourceforge.net/projects/pexpect/")


            if "pexpect" in dir():
                AppServer.app_server_process = pexpect.spawn(command_to_spawn)
                keep_looking = True
                while keep_looking:
                    index = AppServer.app_server_process.expect(["Allow dev_appserver to check for updates on startup?", "Running application", "ERROR", pexpect.EOF, pexpect.TIMEOUT])
                    if index == 0:
                        # The user does not have a nag file yet. Answer Y on their behalf.
                        AppServer.app_server_process.sendline("Y")
                    elif index == 1:
                        # Successful startup!
                        keep_looking = False
                        opened_successfully = True
                    elif index == 2:
                        # The server showed an ERROR message; log it and fail.
                        keep_looking = False
                        opened_successfully = False
                        logging.error("dev_appserver reported an error while starting up.")
                        logging.error("Please start the server manually with the command\n%s\nand resolve the error", startup_command)
                    else:
                        # The server just died or did not give us any hint as to why; log it and fail.
                        keep_looking = False
                        opened_successfully = False
                        logging.error("dev_appserver did not start.")
                        logging.error("Please start the server manually with the command\n%s\nand resolve the error", startup_command)
            else:
                print "Unable to start dev_appserver automatically. Please start it manually for the"
                print "application against which you will be running tests."
                opened_successfully = False
        else:
            # Otherwise, we have been asked to start the server on the
            # port on which it is already running, so leave well-enough
            # alone.
            opened_successfully = True
        
        return opened_successfully
            
    @staticmethod
    def stop():
        if AppServer.app_server_process is not None:
            killed = AppServer.app_server_process.terminate()
            if killed:
                AppServer.app_server_process = None
            else:
                logging.info("Unable to kill the dev_appserver process; please terminate it manually.")
    
# References:
# http://docs.python.org/library/httplib.html#httplib.HTTPResponse
class ActionTestCase(unittest.TestCase):

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)
        
    @staticmethod
    def __build_action_url(controller, action, id, get_values):
        action_path = "/"
        if controller is not None and len(controller) > 0:
            action_path += controller
            
            if action is not None and len(action) > 0:
                action_path += "/%s" % action
                
                if id is not None and len(str(id)) > 0:
                    action_path += "/%s" % str(id)
        
        return ActionTestCase.__build_url(action_path, get_values)
    
    @staticmethod
    def __build_url(url, get_values):
        if get_values is not None and len(get_values) > 0:
            # Add query parameters
            url += "?"
            first_pair = True
            for each_key, each_value in get_values.iteritems():
                if not first_pair:
                    url += "&"
                else:
                    first_pair = False
                url += "%s=%s" % (urllib.quote(each_key), urllib.quote(each_value))
        return url
    
    def run_action(self, controller, action, id, verb, headers, authorization, get_values, post_values):
        self.controller = controller
        self.action = action
        self.id = id
        if verb is not None and len(verb) > 0:
            self.verb = verb
        else:
            self.verb = "GET"
            
        self.headers = headers
        self.get_values = get_values
        self.post_values = post_values
        self.authorization = authorization
            
        self.__requested_authorization = False
        self.__redirected = False
        self.__permanent_redirect = False
        
        keep_going = True
        cookies = []
        
        request_host = "localhost"
        request_port = AppServer.app_server_port
        request_url = ActionTestCase.__build_action_url(self.controller, action, id, get_values)
        request_body = ""
        request_verb = self.verb
        
        original_request_body = ""
        if post_values is not None and len(post_values) > 0:
            original_request_body = urllib.urlencode(post_values)
        request_body = original_request_body
        
        while keep_going:
            headers = {}
            if len(cookies) > 0:
                for each_cookie in cookies:
                    headers["Cookie"] = each_cookie
            self.connection = httplib.HTTPConnection(request_host, request_port)
            self.connection.request(request_verb, request_url, request_body, headers)
            self.response = self.connection.getresponse()
            cookie = self.response.getheader("set-cookie")
            if cookie != None:
                cookies.append(cookie)
                
            if self.response.status == 302 or self.response.status == 301:
                location = self.response.getheader("Location")
                unquoted_location = urllib.unquote(location)
                redirect_location = urlparse(unquoted_location)
                if self.response.status == 301:
                    self.__permanent_redirect = True
                self.__redirected = True
                    
                if location.find("_ah/login") != -1:
                    # The action requires authorization, so send the authorization
                    # credentials, note the fact, and set response to what is
                    # actually returned.
                    if len(authorization) == 2:
                        self.__requested_authorization = True
                        complete_request_values = {}
                        complete_request_values["action"] = "Login"
                        complete_request_values["continue"] = redirect_location.query.split('=')[1]
                        complete_request_values["email"] = authorization["email"]
                        complete_request_values["admin"] = str(authorization["admin"])
                    
                        request_url = ActionTestCase.__build_url("/_ah/login", complete_request_values)
                        request_host = redirect_location.hostname
                        request_port = redirect_location.port
                        request_verb = "GET"
                else:
                    # Redirected somewhere besides the authorization page.
                    request_host = redirect_location.hostname
                    request_port = redirect_location.port
                    request_verb = self.verb
                    request_url = redirect_location.path
                    request_body = original_request_body
            else:
                # On anything besides 301 or 302, consider the request to be complete.
                keep_going = False
                
        self.response_body = self.response.read()
                    
    def assertStatus(self, status):
        """Test that the requested resource returned a specific HTTP Status Code.
        See RFC 2616 (http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html) for details."""
        if status != self.response.status:
            raise self.failureException, "Action returned status of %s, not %s with body\n%s" % (str(self.response.status), str(status), self.response_body)
    
    def assertRequestedAuthorization(self):
        """Test that the requested resource responded by asking for credentials."""
        if self.__requested_authorization == False:
            raise self.failureException, "Action did not request authorization"

    def assertRedirected(self):
        """Test that the requested resource redirected us elsewhere."""
        if self.__redirected == False:
            raise self.failureException, "Action did not redirect."
        
    def assertPermanentlyRedirected(self):
        """Test that the requested resource permanently redirected elsewhere."""
        if self.__permanent_redirect == False:
            raise self.failureException, "Action did not permanently redirect."

    def assertResponseIs(self, response):
        """Test that the requested resource exactly matches a specific string."""
        if self.response_body != response:
            raise self.failureException, "Response (%s) did not match expected result (%s)" % (self.response_body, response)
    
    def assertResponseIsEmpty(self):
        """Test that the requested resource returns an empty body."""
        if len(self.response_body) != 0:
            raise self.failureException, "Response was not empty"
    def assertResponseIsNotEmpty(self):
        """Test that the requested resource returns a non-empty body."""
        if len(self.response_body) == 0:
            raise self.failureException, "Response was empty"
    
    def assertResponseContains(self, contained):
        """Test that the response contains the given string or list of strings.
        If a list of strings is given, they must appear in the response in the
        order in which they appear in the list."""
        
        does_contain = True
        
        # Make sure that we are dealing with an iterable list, even if the
        # calling code is only looking for a single string.
        if type(contained) is not list:
            contained = [contained]
        
        found_at = 0
        for each_contained in contained:
            found_at = self.response_body.find(each_contained, found_at)
            if found_at == -1:
                does_contain = False
                break
            else:
                found_at += len(each_contained)
        
        return does_contain

def main():
    AppServer.start()
    unittest.main()
    AppServer.stop()