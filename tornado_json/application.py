import tornado.web.Application

from tornado_json import db
from tornado_json.api_doc_gen import api_doc_gen


class Application(tornado.web.Application):

    """Entry-point for the app"""

    def __init__(self, routes, settings):
        """
        - Generate API documentation using provided routes
        - Initialize the application
        - Create connection to the DB

        :type  routes: [(str, RequestHandler), ... ]
        :param rotues: List of routes for the app
        :type  settings: dict
        :param settings: Settings for the app
        """
        # Generate API Documentation
        api_doc_gen(routes)

        # Unless gzip was specifically set to False in settings, enable it
        if "gzip" not in settings.keys():
            settings["gzip"] = True

        tornado.web.Application.__init__(
            self,
            routes,
            **settings
        )

        self.db_conn = db.Connection()
