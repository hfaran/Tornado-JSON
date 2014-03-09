==========================
Request Handler Guidelines
==========================

Schemas and Public API Documentation
------------------------------------

Use the ``schema.validate`` decorator on methods which will automatically
validate the request body and output against the schemas provided. The schemas
must be valid JSON schemas;
`readthedocs <https://python-jsonschema.readthedocs.org/en/latest/>`__
for an example.
Additionally, ``return`` the data from the
request handler, rather than writing it back (the decorator will take
care of that).

The docstring of the method, as well as the schemas will be used to generate
**public** API documentation.

.. code:: python

    class ExampleHandler(APIHandler):
        @schema.validate(input_schema=..., output_schema=...)
        def post(self):
            """I am the public API documentation of this route"""
            ...
            return data


Assertions
----------


Use ``exceptions.api_assert`` to fail when some the client does not meet some
API pre-condition/requirement, e.g., an invalid or incomplete request is
made. When using an assertion is not suitable,
``raise APIError( ... )``; don't use ``self.fail`` directly.

.. code:: python

    class ExampleHandler(APIHandler):
        @schema.validate()
        def post(self):
            ...
            api_assert(condition, status_code, log_message=log_message)
