import sys

from tornado import version_info as tornado_version_info


PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2

(TORNADO_MAJOR,
 TORNADO_MINOR,
 TORNADO_PATCH) = tornado_version_info[:3]

HTTP_METHODS = ["get", "put", "post", "patch", "delete", "head", "options"]
