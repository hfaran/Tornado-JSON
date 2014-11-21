from tornado import version_info as tornado_version_info


(TORNADO_MAJOR,
 TORNADO_MINOR,
 TORNADO_PATCH) = tornado_version_info[:3]

HTTP_METHODS = ["get", "put", "post", "patch", "delete", "head", "options"]
