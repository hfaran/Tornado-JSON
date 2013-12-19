# TODO: Better organization for contents of this module

import json
import logging
from jsonschema import validate, ValidationError

from tornado.web import HTTPError


class APIError(HTTPError):

    """Equivalent to RequestHandler.HTTPError except for in name"""


def api_assert(condition, *args, **kwargs):
    """Asserts that condition is True, else raises an APIError with the
    provided args and kwargs

    :type  condition: bool
    """
    if not condition:
        raise APIError(*args, **kwargs)


def io_schema(method_name):
    """Decorator for RequestHandler schema validation

    This decorator:
        - Validates request body against in_schema
        - Calls the rh_method and gets output from it
        - Validates output against out_schema
        - Calls JSendMixin.success to write the validated output

    :type  method_name: str
    :param method_name: Name of the requesthandler method that
       the io_schema is decorating
    :returns: The decorated method
    """
    def _decorator(rh_method):
        def _wrapper(self, *args, **kwargs):
            # Special case for GET request (since there is no data to validate)
            if method_name.lower() not in ["get"]:
                # If input is not valid JSON, fail
                try:
                    input_ = json.loads(self.request.body)
                except ValueError as e:
                    logging.error(str(e))
                    self.fail(str(e))
                    return

                # Validate the received input
                validate(input_, type(self)
                         .api_documentation[method_name]["input_schema"])
            else:
                input_ = None

            # Call the requesthandler method
            output = rh_method(self, input_)

            # We wrap output in an object before validating in case
            #  output is a string (and ergo not a validatable JSON object)
            try:
                validate(
                    {"result": output},
                    {
                        "type": "object",
                        "properties": {
                            "result": type(self)
                            .api_documentation[method_name]["output_schema"]
                        },
                        "required": ["result"]
                    }
                )
            except ValidationError as e:
                # We essentially re-raise this as a TypeError because
                #  we don't want this error data passed back to the client
                #  because it's a fault on our end. The client should
                #  only see a 500 - Internal Server Error.
                raise TypeError(str(e))

            # If no ValidationError has been raised up until here, we write
            #  back output
            self.success(output)
        return _wrapper
    return _decorator
