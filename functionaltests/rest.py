import urllib2_file
from urllib2 import urlopen

from twill.errors import TwillAssertionError

# singleton restcontext per extend_with 
class restContext(object):
    lastContentResponse = None
    keyvalues = {}
    verbose = True
    
    def __call__(self):
        return self
    
    def compileString(self,value):
        for k, v in self.keyvalues.iteritems():
            value = value.replace(k, v)
        return value
        
    def assertContains(self,value,content,origin):
        self.lastContentResponse = content
        if self.verbose:
            print content
        
        if content.find(value) == -1: 
            raise TwillAssertionError(content+" found instead of "+value+" in response of " + self.compileString(origin))
        
    def assertNotContains(self, value,content,origin):
        self.lastContentResponse = content
        if self.verbose:
            print content
            
        if content.find(value) != -1:
            raise TwillAssertionError(value+" found in "+content+" in response of " + self.compileString(origin))
        
# singleton instance 
restContext = restContext()

# usage within twill : assertGet http://localhost:8080/something?asdasd
def assertGetContains(*args):
    if restContext.verbose:
        print "GET "+restContext.compileString(args[1])
    content = urlopen(restContext.compileString(args[1])).read()
    restContext.assertContains(args[0], content, args[1])

# usage within twill : assertGet http://localhost:8080/something?asdasd
def assertGetNotContains(*args):
    if restContext.verbose:
        print "GET "+restContext.compileString(args[1])
    content = urlopen(restContext.compileString(args[1])).read()
    restContext.assertNotContains(args[0], content, args[1])
    
# usage within twill : assertPostContains TESTVALUE http://localhost:8080/something url=value&url2=value2
def assertPostContains(*args):
    if restContext.verbose:
        print "POST "+restContext.compileString(args[1])+" & "+restContext.compileString(args[2])
    content = urlopen(restContext.compileString(args[1]),restContext.compileString(args[2])).read()
    restContext.assertContains(args[0], content, args[1])

# usage within twill : assertPostNotContains TESTVALUE http://localhost:8080/something url=value&url2=value2
def assertPostNotContains(*args):
    if restContext.verbose:
        print "POST "+restContext.compileString(args[1])+" & "+restContext.compileString(args[2])
    content = urlopen(restContext.compileString(args[1]),restContext.compileString(args[2])).read()
    restContext.assertNotContains(args[0], content, args[1])

# usage within twill : assertUploadFileNotContains TESTVALUE http://localhost:8080/something fileName filePath
def assertUploadFileContains(*args):
    if restContext.verbose:
        print "UPLOAD "+restContext.compileString(args[1])+" & "+restContext.compileString(args[2])+"->"+restContext.compileString(args[3])
    data = {restContext.compileString(args[2]): open(restContext.compileString(args[3]))}
    content = urlopen(restContext.compileString(args[1]),data).read()
    restContext.assertContains(args[0], content, args[1])
    
# usage within twill : assertUploadFileNotContains TESTVALUE http://localhost:8080/something fileName filePath
def assertUploadFileNotContains(*args):
    if restContext.verbose:
        print "UPLOAD "+restContext.compileString(args[1])+" & "+restContext.compileString(args[2])+"->"+restContext.compileString(args[3])
    data = {restContext.compileString(args[2]): open(restContext.compileString(args[3]))}
    content = urlopen(restContext.compileString(args[1]),data).read()
    restContext.assertNotContains(args[0], content, args[1])