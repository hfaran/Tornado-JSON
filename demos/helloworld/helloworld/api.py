from tornado_json.requesthandlers import APIHandler
from tornado_json.utils import io_schema


class HelloWorldHandler(APIHandler):

    apid = {
        "get": {
            "input_schema": None,
            "output_schema": {
                "type": "string",
            },
            "doc": "Shouts hello to the world!"
        },

    }

    @io_schema
    def get(self, body):
        return "Hello world!"
