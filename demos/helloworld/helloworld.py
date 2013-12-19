#!/usr/bin/env python2.7

# The following so demo can be run without having to install package #
import sys
sys.path.append("../../")
# Can be removed if Tornado-JSON is installed #

import tornado.ioloop

from tornado_json.application import Application
from tornado_json.requesthandlers import APIHandler
from tornado_json.utils import io_schema


class HelloWorldHandler(APIHandler):

    api_documentation = {
        "get": {
            "input_schema": None,
            "output_schema": {
                "type": "string",
            },
            "doc": "Shouts hello to the world!"
        },

    }

    @io_schema("get")
    def get(self, body):
        return "Hello world!"


def main():
    routes = [(r"/", HelloWorldHandler)]
    application = Application(routes=routes, settings={})
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
