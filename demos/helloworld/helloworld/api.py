from tornado_json.requesthandlers import APIHandler
from tornado_json.utils import io_schema


class HelloWorldHandler(APIHandler):

    apid = {
        "get": {
            "input_schema": [None],
            "output_schema": {
                "type": "string",
            },
            "output_example": "Hello world!",
            "input_example": [None],
            "doc": "Shouts hello to the world!",
        },
    }

    @io_schema
    def get(self):
        return "Hello world!"


class Greeting(APIHandler):

    apid = {
        "get": {
            "input_schema": [None],
            "output_schema": {
                "type": "string",
            },
            "output_example": "Greetings, Greg!",
            "input_example": [None],
            "doc": "Greets you.",
        },
    }

    # When you include extra arguments in the signature of an HTTP
    #   method, Tornado-JSON will generate a route that matches the extra
    #   arguments; here, you can GET /api/greeting/Greg and you will
    #   get a response back that says, "Greetings, Greg!"
    @io_schema
    def get(self, name):
        return "Greetings, {}!".format(name)
