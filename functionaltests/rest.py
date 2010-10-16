from urllib2 import urlopen

from twill.errors import TwillAssertionError

# usage within twill : assertGet http://localhost:8080/something?asdasd
def assertGetContains(*args):
    content = urlopen(args[1]).read()
    value = content.find(args[0]) != -1
    if value != True:
        raise TwillAssertionError(args[0]+" not contained in response of " + args[1])

# usage within twill : assertGet http://localhost:8080/something?asdasd
def assertGetNotContains(*args):
    content = urlopen(args[1]).read()
    value = content.find(args[0]) != -1
    if value != False:
        raise TwillAssertionError(args[0]+" contained in response of " + args[1])
    
# usage within twill : assertPostContains TESTVALUE http://localhost:8080/something [url: 'http://python.org', tags:['python']]
def assertPostContains(*args):
    content = urlopen(args[1],args[2]).read()
    value = content.find(args[0]) != -1
    if value != True: 
        raise TwillAssertionError(args[0]+" not contained in response of " + args[1])

# usage within twill : assertPostNotContains TESTVALUE http://localhost:8080/something [url: 'http://python.org', tags:['python']]
def assertPostNotContains(*args):
    content = urlopen(args[1],args[2]).read()
    value = content.find(args[0]) != -1
    if value != False: 
        raise TwillAssertionError(args[0]+" contained in response of " + args[1])

