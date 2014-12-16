import sys

from tornado import version_info as tornado_version_info


#######################
# Version Definitions #
#######################

PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2
TORNADO_MAJOR, TORNADO_MINOR, TORNADO_PATCH = tornado_version_info[:3]


############################
# Python 2/3 compatibility #
############################

if PY3:
     unicode = str
     basestring = (str, bytes)
     bytes = bytes
elif PY2:
     unicode = unicode
     basestring = basestring
     bytes = str


################
# Tornado-JSON #
################

HTTP_METHODS = ["get", "put", "post", "patch", "delete", "head", "options"]
