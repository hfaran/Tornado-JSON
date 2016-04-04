import json

try:
    from UserDict import UserDict
except ImportError:
    from collections import UserDict

from functools import wraps

import jsonschema

import tornado.gen

from tornado_json.exceptions import APIError

try:
    from tornado.concurrent import is_future
except ImportError:
    # For tornado 3.x.x
    from tornado.concurrent import Future
    is_future = lambda x: isinstance(x, Future)

from tornado_json.utils import container


def schemahelpers_as_dict(schema, requesthandler):
    """Return schema copy with all (nested too) SchemaHelper processed as a
    dict."""
    d = {}
    for k, v in schema.items():
        if isinstance(v, SchemaHelper):
            d[k] = v.as_dict(requesthandler)
        elif isinstance(v, dict):
            d[k] = schemahelpers_as_dict(v, requesthandler)
        else:
            d[k] = v
    return d


class SchemaHelper(UserDict):
    """Helper class to create dynamic schemas in an elegant way.

    SchemaHelper is a just an extend dict with method "as_dict", this methods
    returns the dict itself updated the result of all methods that match the
    pattern above:

    get_%(key)s_key as dict[%(key)s]

    :Example:

    >>> class MySchema(SchemaHelper):
    ...     def get_type_key(self):
    ...         return "object"
    >>>
    >>> myschema = MySchema()
    >>> myschema.as_dict()
    {"type": "object"}
    """

    def as_dict(self, requesthandler=None):
        """Return a dict containing the SchemaHelper processed methods.

        :param requesthandler: Tornado request handler instance
        :type tornado.web.RequestHandler:
        :returns: dict to be used on jsonschema
        :rtype: dict
        """
        d = {}

        for attrname in dir(self):
            if attrname.startswith("get_") and attrname.endswith("_key"):
                method = getattr(self, attrname)
                if callable(method):
                    k = attrname[4:-4]
                    v = method(requesthandler)
                    if isinstance(v, SchemaHelper):
                        v = v.as_dict(requesthandler)
                    d[k] = v

        d = schemahelpers_as_dict(d, requesthandler)

        return d


@tornado.gen.coroutine
def evaluate_schema_callbacks(schema):
    """Return schema with all schema callbacks evaluated.

    :param schema: schema with callback(s)
    :type schema: dict
    :returns: schema evaluated
    :rtype: dict
    """
    d = {}
    for k, v in schema.items():
        if isinstance(v, SchemaCallback):
            v = v()
        elif isinstance(v, dict):
            v = yield evaluate_schema_callbacks(v)
        d[k] = v
    raise tornado.gen.Return(d)


def detect_schemacallback(schema):
    """Check recursively if the schema has a SchemaCallback instance."""
    for k, v in schema.items():
        if isinstance(v, SchemaCallback):
            return True
        elif isinstance(v, dict):
            if detect_schemacallback(v):
                return True

    return False


class SchemaCallback(object):
    """Class to create dynamic key values on schemas."""

    def __init__(self, func, *args, **kwargs):
        """Store the callable with args and kwargs.

        :param func: callable method
        :param args: args to be passsed to func
        :params kwargs: kwargs to be passed to func
        :type func: callable
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        """Call the function asynchronously trought tornado.gen.Task class."""
        return self.func(*self.args, **self.kwargs)


def validate(input_schema=None, output_schema=None,
             input_example=None, output_example=None,
             validator_cls=None,
             format_checker=None, on_empty_404=False):
    """Parameterized decorator for schema validation.

    :type validator_cls: IValidator class
    :type format_checker: jsonschema.FormatChecker or None
    :type on_empty_404: bool
    :param on_empty_404: If this is set, and the result from the
        decorated method is a falsy value, a 404 will be raised.
    """

    input_schema_has_callback = False
    if input_schema is not None:
        input_schema_has_callback = detect_schemacallback(input_schema)

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
        :raises APIError: If the output is a falsy value and
            on_empty_404 is True, an HTTP 404 error is returned
        """
        @wraps(rh_method)
        @tornado.gen.coroutine
        def _wrapper(self, *args, **kwargs):
            # In case the specified input_schema is ``None``, we
            #   don't json.loads the input, but just set it to ``None``
            #   instead.
            input_schema = _wrapper.input_schema
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

                # if isinstance(input_schema, SchemaHelper):
                #     input_schema = input_schema.as_dict(self, *args, **kw)

                if input_schema_has_callback:
                    input_schema = \
                        yield evaluate_schema_callbacks(input_schema)

                # Validate the received input
                jsonschema.validate(
                    input_,
                    input_schema,
                    cls=validator_cls,
                    format_checker=format_checker
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

            # if output is empty, auto return the error 404.
            if not output and on_empty_404:
                raise APIError(404, "Resource not found.")

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
