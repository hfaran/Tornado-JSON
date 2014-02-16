# TODO: Better organization for contents of this module

import json
import logging
from jsonschema import validate, ValidationError

from tornado.web import HTTPError


class APIError(HTTPError):

    """Equivalent to RequestHandler.HTTPError except for in name"""


def api_assert(condition, *args, **kwargs):
    """Asserts that `condition` is `True`, else raises an `APIError` with the
    provided `args` and `kwargs`

    :type  condition: bool
    """
    if not condition:
        raise APIError(*args, **kwargs)


def container(dec):
    """Meta-decorator (for decorating decorators)

    Keeps around original decorated function as a property `orig_func`
    Credits: http://stackoverflow.com/a/1167248/1798683
    """
    def meta_decorator(f):
        decorator = dec(f)
        decorator.orig_func = f
        return decorator
    return meta_decorator


@container
def io_schema(rh_method):
    """Decorator for RequestHandler schema validation

    This decorator:
        - Validates request body against input schema of the method
        - Calls the `rh_method` and gets output from it
        - Validates output against output schema of the method
        - Calls `JSendMixin.success` to write the validated output

    :type  rh_method: function
    :param rh_method: The RequestHandler method to be decorated
    :returns: The decorated method
    """

    def _wrapper(self, *args, **kwargs):
        # Get name of method
        method_name = rh_method.__name__

        # Special case for GET, DELETE requests (since there is no data to validate)
        if method_name not in ["get", "delete"]:
            # If input is not valid JSON, fail
            try:
                input_ = json.loads(self.request.body)
            except ValueError as e:
                logging.error(str(e))
                self.fail(str(e))
                return

            # Validate the received input
            validate(input_, type(self)
                     .apid[method_name]["input_schema"])
        else:
            input_ = None

        # A json.loads'd version of self.request["body"] is now available
        #   as self.body
        setattr(self, "body", input_)
        # Call the requesthandler method
        output = rh_method(self, *args, **kwargs)

        # We wrap output in an object before validating in case
        #  output is a string (and ergo not a validatable JSON object)
        try:
            validate(
                {"result": output},
                {
                    "type": "object",
                    "properties": {
                        "result": type(self)
                        .apid[method_name]["output_schema"]
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
