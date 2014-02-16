Using Tornado-JSON
==================

A Simple Hello World JSON API
-----------------------------

I'll be referencing the
`helloworld <https://github.com/hfaran/Tornado-JSON/tree/master/demos/helloworld>`__
example in the ``demos`` for this.

We want to do a lot of the same things we'd usually do when creating a
Tornado app with a few differences.

helloworld.py
~~~~~~~~~~~~~

First, we'll import the required packages:

.. code:: python

    import tornado.ioloop
    from tornado_json.routes import get_routes
    from tornado_json.application import Application

Next we'll import the package containing our web app. This is the
package where all of your RequestHandlers live.

.. code:: python

    import helloworld

Next, we write a lot of the same Tornado "boilerplate" as you'd find in
the Tornado helloworld example, except, you don't have to manually
specify routes because ``tornado_json`` gathers those for you and names
them based on your project structure and RequestHandler names. You're
free to customize ``routes`` however you want, of course, after they've
been initially automatically generated.

.. code:: python

    def main():
        # Pass the web app's package the get_routes and it will generate
        #   routes based on the submodule names and ending with lowercase
        #   request handler name (with 'handler' removed from the end of the
        #   name if it is the name).
        # [("/api/helloworld", helloworld.api.HelloWorldHandler)]
        routes = get_routes(helloworld)

        # Create the application by passing routes and any settings
        application = Application(routes=routes, settings={})

        # Start the application on port 7777
        application.listen(7777)
        tornado.ioloop.IOLoop.instance().start()

helloworld/api.py
~~~~~~~~~~~~~~~~~

Now comes the fun part where we develop the actual web app. We'll import
``APIHandler`` (this is the handler you should subclass for API routes),
and the ``io_schema`` decorator which will validate input and output
schema for us.

.. code:: python

    from tornado_json.requesthandlers import APIHandler
    from tornado_json.utils import io_schema

    class HelloWorldHandler(APIHandler):
        """Hello!"""
        # apid
        # get(...)

Next, we'll define the ``apid`` class variable. ``apid`` is where we'll
store the input and output schema for each HTTP method as well as the
public API documentation for that route which will be automatically
generated when you run the app (see the Documentation Generation section
for details). Input and output schemas are as per the `JSON
Schema <http://json-schema.org/>`__ standard.

.. code:: python

        apid = {
            "get": {
                "input_schema": None,
                "output_schema": {
                    "type": "string",
                },
                "doc": "Shouts hello to the world!"
            },
        }

Finally we'll write our ``get`` method which will write "Hello world!"
back. Notice that rather than using ``self.write`` as we usually would,
we simply return the data we want to write back, which will then be
validated against the output schema and be written back according to the
`JSend <http://labs.omniti.com/labs/jsend>`__ specification. The
``io_schema`` decorator handles all of this so be sure to decorate any
HTTP methods with it.

.. code:: python

        @io_schema
        def get(self, body):
            return "Hello world!"

Running our Hello World app
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, we can finally run the app ``python helloworld.py``. You should be
able to send a GET request to ``localhost:7777/api/helloworld`` and get
a JSONic "Hello world!" back. Additionally, you'll notice an
``API_Documentation.md`` pop up in the directory, which contains the API
Documentation you can give to users about your new and fantastic API.
