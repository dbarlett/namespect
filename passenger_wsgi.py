#!env/bin/python

import sys, os
INTERP = os.path.join(os.getcwd(), 'env', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())
from core import app

# hackish way to make Passenger urldecode the same way WSGI does
import urllib2
def application(environ, start_response):
    environ["PATH_INFO"] = urllib2.unquote(environ["PATH_INFO"])
    return app(environ, start_response)
