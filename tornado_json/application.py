import tornado.web

from tornado_json.api_doc_gen import api_doc_gen


class Application(tornado.web.Application):

    """Entry-point for the app

    - Generate API documentation using provided routes
    - Initialize the application

    :type  routes: [(url, RequestHandler), ...]
    :param routes: List of routes for the app
    :type  settings: dict
    :param settings: Settings for the app
    :param  db_conn: Database connection
    """

    def __init__(self, routes, settings, db_conn=None):
        # Generate API Documentation
        api_doc_gen(routes)

        # Unless gzip was specifically set to False in settings, enable it
        if "gzip" not in list(settings.keys()):
            settings["gzip"] = True

        tornado.web.Application.__init__(
            self,
            routes,
            **settings
        )

        self.db_conn = db_conn
