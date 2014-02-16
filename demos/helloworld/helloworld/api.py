from tornado import gen

from tornado_json.requesthandlers import APIHandler
from tornado_json.utils import io_schema


class HelloWorldHandler(APIHandler):

    apid = {
        "get": {
            "input_schema": None,
            "output_schema": {
                "type": "string",
            },
            "output_example": "Hello world!",
            "input_example": None,
            "doc": "Shouts hello to the world!",
        },
    }

    # Decorate any HTTP methods with the `io_schema` decorator
    #   to validate input to it and output from it as per the
    #   the schema for the method defined in `apid`
    # Simply use `return` rather than `self.write` to write back
    #   your output.
    @io_schema
    def get(self):
        return "Hello world!"


class AsyncHelloWorld(APIHandler):

    apid = {
        "get": {
            "input_schema": None,
            "output_schema": {
                "type": "string",
            },
            "output_example": "Hello (asynchronous) world!",
            "input_example": None,
            "doc": "Shouts hello to the world (asynchronously)!",
        },
    }

    def hello(self, callback=None):
        callback("Hello (asynchronous) world!")

    @io_schema
    @gen.coroutine
    def get(self):
        # Asynchronously yield a result from a method
        res = yield gen.Task(self.hello)

        # When using the io_schema decorator asynchronously,
        #   we can return the output desired by raising
        #   `tornado.gen.Return(value)` which returns a
        #   Future that the decorator will yield.
        # In Python 3.3, using `raise Return(value)` is no longer
        #   necessary and can be replaced with simply `return value`.
        #   For details, see:
        #   http://www.tornadoweb.org/en/branch3.2/gen.html#tornado.gen.Return

        # return res  # Python 3.3
        raise gen.Return(res)  # Python 2.7


class Greeting(APIHandler):

    apid = {
        "get": {
            "input_schema": None,
            "output_schema": {
                "type": "string",
            },
            "output_example": "Greetings, Greg!",
            "input_example": None,
            "doc": "Greets you.",
        },
    }

    # When you include extra arguments in the signature of an HTTP
    #   method, Tornado-JSON will generate a route that matches the extra
    #   arguments; here, you can GET /api/greeting/Greg and you will
    #   get a response back that says, "Greetings, Greg!"
    # You can match the regex equivalent of `\w+`.
    @io_schema
    def get(self, name):
        return "Greetings, {}!".format(name)
