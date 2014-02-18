from tornado import gen

from tornado_json.requesthandlers import APIHandler
from tornado_json import schema


class HelloWorldHandler(APIHandler):

    apid = {}
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "string",
        },
        "output_example": "Hello world!",
        "input_example": None,
        "doc": "Shouts hello to the world!",
    }

    # Decorate any HTTP methods with the `schema.validate` decorator
    #   to validate input to it and output from it as per the
    #   the schema for the method defined in `apid`
    # Simply use `return` rather than `self.write` to write back
    #   your output.
    @schema.validate
    def get(self):
        return "Hello world!"


class AsyncHelloWorld(APIHandler):

    apid = {}
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "string",
        },
        "output_example": "Hello (asynchronous) world!",
        "input_example": None,
        "doc": "Shouts hello to the world (asynchronously)!",
    }

    def hello(self, callback=None):
        callback("Hello (asynchronous) world!")

    @schema.validate
    @gen.coroutine
    def get(self):
        # Asynchronously yield a result from a method
        res = yield gen.Task(self.hello)

        # When using the `schema.validate` decorator asynchronously,
        #   we can return the output desired by raising
        #   `tornado.gen.Return(value)` which returns a
        #   Future that the decorator will yield.
        # In Python 3.3, using `raise Return(value)` is no longer
        #   necessary and can be replaced with simply `return value`.
        #   For details, see:
        # http://www.tornadoweb.org/en/branch3.2/gen.html#tornado.gen.Return

        # return res  # Python 3.3
        raise gen.Return(res)  # Python 2.7


class PostIt(APIHandler):

    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
                "index": {"type": "number"},
            },
        },
        "input_example": {
            "title": "Very Important Post-It Note",
            "body": "Equally important message",
            "index": 0
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        },
        "output_example": {
            "message": "Very Important Post-It Note was posted."
        },
        "doc": """
POST the required parameters to post a Post-It note

* `title`: Title of the note
* `body`: Body of the note
* `index`: An easy index with which to find the note
"""
    }

    @schema.validate
    def post(self):
        # `schema.validate` will JSON-decode `self.request.body` for us
        #   and set self.body as the result, so we can use that here
        return {
            "message": "{} was posted.".format(self.body["title"])
        }


class Greeting(APIHandler):

    apid = {}
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "string",
        },
        "output_example": "Greetings, Named Person!",
        "input_example": None,
        "doc": "Greets you.",
    }

    # When you include extra arguments in the signature of an HTTP
    #   method, Tornado-JSON will generate a route that matches the extra
    #   arguments; here, you can GET /api/greeting/John/Smith and you will
    #   get a response back that says, "Greetings, John Smith!"
    # You can match the regex equivalent of `\w+`.
    @schema.validate
    def get(self, fname, lname):
        return "Greetings, {} {}!".format(fname, lname)


class FreeWilledHandler(APIHandler):

    # And of course, you aren't forced to use schema validation;
    #   if you want your handlers to do something more custom,
    #   they definitely can.
    def get(self):
        # If you don't know where `self.success` comes from, it is defined
        #   in the `JSendMixin` mixin in tornado_json.jsend. `APIHandler`
        #   inherits from this and thus gets the methods.
        self.success("I don't need no stinkin' schema validation.")
        # If you're feeling really bold, you could even skip JSend
        #   altogether and do the following EVIL thing:
        # self.write("I'm writing back a string that isn't JSON! Take that!")
