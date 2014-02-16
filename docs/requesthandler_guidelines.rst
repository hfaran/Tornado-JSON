==========================
Request Handler Guidelines
==========================

Schemas and Public API Documentation
------------------------------------

Create an ``apid`` dict in each RequestHandler as a class-level
variable, i.e.,

.. code:: python

    class ExampleHandler(APIHandler):
        apid = {}

For each HTTP method you implement, add a corresponding entry in
``apid``. The schemas must be valid JSON schemas;
`readthedocs <https://python-jsonschema.readthedocs.org/en/latest/>`__
for an example. Here is an example for POST:

.. code:: python

    apid["post"] = {
        "input_schema": ...,
        "output_schema": ...,
        "doc": ...,
    }

``doc`` is the **public** accompanying documentation that will be
available on the wiki.

Use the ``io_schema`` decorator on methods which will automatically
validate the request body and output against the schemas in
``apid[method_name]``. Additionally, ``return`` the data from the
request handler, rather than writing it back (the decorator will take
care of that).

.. code:: python

    class ExampleHandler(APIHandler):
        @io_schema
        def post(self):
            ...
            return data


Assertions
----------


Use ``utils.api_assert`` to fail when some the client does not meet some
API pre-condition/requirement, e.g., an invalid or incomplete request is
made. When using an assertion is not suitable,
``raise APIError( ... )``; don't use JSend ``fail`` directly.

.. code:: python

    class ExampleHandler(APIHandler):
        @io_schema
        def post(self):
            ...
            api_assert(condition, status_code, log_message=log_message)
