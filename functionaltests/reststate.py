from rest import restContext
from xml2obj import xml2obj
import sys
import time

from twill.errors import TwillAssertionError

def wait(*args):
    if restContext.verbose:
        print "waiting for "+args[0]+" secs"
    time.sleep(float(args[0]))

def xmlparseLastResponseWith(*args):
    try:
        if restContext.verbose:
            print "parsing xml response with "+args[0]+"@"+args[1]
        mod = __import__(args[0])
        func = getattr(mod, args[1])
        func(xml2obj(restContext.lastContentResponse), restContext.keyvalues)
    except Exception as inst:
        raise TwillAssertionError("at "+args[0]+" could not be called "+args[1]+" due \""+inst.__str__()+"\"")