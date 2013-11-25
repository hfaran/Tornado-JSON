import re
import logging
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado import web
from tornado.options import define, options

from touchpoint import db
from touchpoint.signup import routes as signup_routes
from touchpoint.api_doc_gen import api_doc_gen


define("port", default=8888, help="run on the given port", type=int)
define("log_file", default="/var/log/touchpoint/touchpoint.log",
       help="path for the log file", type=str)


class Application(tornado.web.Application):

    """Entry-point for the app"""

    def __init__(self):
        """
        - Gather all routes
        - Generate API documentation using gathered routes
        - Initialize the application
        - Create connection to the DB
        """
        routes = []
        routes += signup_routes.get_routes()

        # Generate API Documentation
        api_doc_gen(routes)

        settings = dict(
            template_path=os.path.join(
                os.path.dirname(__file__), "../templates"),
            static_path=os.path.join(os.path.dirname(__file__), "../static"),
            gzip=True
        )

        tornado.web.Application.__init__(
            self,
            routes,
            **settings
        )

        self.db_conn = db.Connection()


def main(args=None):
    """
    - Get options from sources (currently just command-line)
    - Create the server
    - Start the server

    :param  args: commandline args (literally sys.argv)
    """
    if not args:
        import sys
        args = sys.argv

    print("Getting ready . . .")
    args.append('--log_file_prefix={}'.format(options.log_file))
    tornado.options.parse_command_line(args)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print("Welcome to Touchpoint")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
