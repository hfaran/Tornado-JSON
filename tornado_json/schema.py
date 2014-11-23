import json
from functools import wraps

import jsonschema
import tornado.gen
try:
    from tornado.concurrent import is_future
except ImportError:
    # For tornado 3.x.x
    from tornado.concurrent import Future
    is_future = lambda x: isinstance(x, Future)

from tornado_json.utils import container


def validate(input_schema=None, output_schema=None,
             input_example=None, output_example=None):
    @container
    def _validate(rh_method):
        """Decorator for RequestHandler schema validation

        This decorator:

            - Validates request body against input schema of the method
            - Calls the ``rh_method`` and gets output from it
            - Validates output against output schema of the method
            - Calls ``JSendMixin.success`` to write the validated output

        :type  rh_method: function
        :param rh_method: The RequestHandler method to be decorated
        :returns: The decorated method
        :raises ValidationError: If input is invalid as per the schema
            or malformed
        :raises TypeError: If the output is invalid as per the schema
            or malformed
        """
        @wraps(rh_method)
        @tornado.gen.coroutine
        def _wrapper(self, *args, **kwargs):
            # In case the specified input_schema is ``None``, we
            #   don't json.loads the input, but just set it to ``None``
            #   instead.
            if input_schema is not None:
                # Attempt to json.loads the input
                try:
                    # TODO: Assuming UTF-8 encoding for all requests,
                    #   find a nice way of determining this from charset
                    #   in headers if provided
                    encoding = "UTF-8"
                    input_ = json.loads(self.request.body.decode(encoding))
                except ValueError as e:
                    raise jsonschema.ValidationError(
                        "Input is malformed; could not decode JSON object."
                    )
                # Validate the received input
                jsonschema.validate(
                    input_,
                    input_schema
                )
            else:
                input_ = None

            # A json.loads'd version of self.request["body"] is now available
            #   as self.body
            setattr(self, "body", input_)
            # Call the requesthandler method
            output = rh_method(self, *args, **kwargs)
            # If the rh_method returned a Future a la `raise Return(value)`
            #   we grab the output.
            if is_future(output):
                output = yield output

            if output_schema is not None:
                # We wrap output in an object before validating in case
                #  output is a string (and ergo not a validatable JSON object)
                try:
                    jsonschema.validate(
                        {"result": output},
                        {
                            "type": "object",
                            "properties": {
                                "result": output_schema
                            },
                            "required": ["result"]
                        }
                    )
                except jsonschema.ValidationError as e:
                    # We essentially re-raise this as a TypeError because
                    #  we don't want this error data passed back to the client
                    #  because it's a fault on our end. The client should
                    #  only see a 500 - Internal Server Error.
                    raise TypeError(str(e))

            # If no ValidationError has been raised up until here, we write
            #  back output
            self.success(output)

        setattr(_wrapper, "input_schema", input_schema)
        setattr(_wrapper, "output_schema", output_schema)
        setattr(_wrapper, "input_example", input_example)
        setattr(_wrapper, "output_example", output_example)

        return _wrapper
    return _validate
