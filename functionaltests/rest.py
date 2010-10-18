from urllib2 import urlopen

from twill.errors import TwillAssertionError
import uuid

def compileString(value):
    if value.find("[%uuid()%]") != -1:
        return value.replace("[%=uuid()%]", uuid.uuid4())
    else:
        return value

# usage within twill : assertGet http://localhost:8080/something?asdasd
def assertGetContains(*args):
    content = urlopen(compileString(args[1])).read()
    value = content.find(args[0]) != -1
    if value != True:
        raise TwillAssertionError(args[0]+" found instead "+content+" in response of " + args[1])

# usage within twill : assertGet http://localhost:8080/something?asdasd
def assertGetNotContains(*args):
    content = urlopen(compileString(args[1])).read()
    value = content.find(args[0]) != -1
    if value != False:
        raise TwillAssertionError(args[0]+" found instead "+content+" in response of " + args[1])
    
# usage within twill : assertPostContains TESTVALUE http://localhost:8080/something url=value&url2=value2
def assertPostContains(*args):
    content = urlopen(compileString(args[1]),compileString(args[2])).read()
    value = content.find(args[0]) != -1
    if value != True: 
        raise TwillAssertionError(args[0]+" found instead "+content+" in response of " + args[1])

# usage within twill : assertPostNotContains TESTVALUE http://localhost:8080/something url=value&url2=value2
def assertPostNotContains(*args):
    content = urlopen(compileString(args[1]),compileString(args[2])).read()
    value = content.find(args[0]) != -1
    if value != False: 
        raise TwillAssertionError(args[0]+" found instead "+content+" in response of " + args[1])

