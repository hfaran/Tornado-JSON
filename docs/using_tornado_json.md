# Using Tornado-JSON

## A Simple Hello World JSON API

I'll be referencing the [`helloworld`](https://github.com/hfaran/Tornado-JSON/tree/dev/demos/helloworld) example in the `demos` for this.

We want to do a lot of the same things we'd usually do when creating a Tornado app with a few differences.

### helloworld.py

First, we'll import the required packages:

```python
import tornado.ioloop
from tornado_json.routes import get_routes
from tornado_json.application import Application
```

Next we'll import the package containing our web app. This is the package where all of your RequestHandlers live.

```python
import helloworld
```

Next, we write a lot of the same Tornado "boilerplate" as you'd find in the Tornado helloworld example, except, you don't have to manually specify routes because `tornado_json` gathers those for you and names them based on your project structure and RequestHandler names. You're free to customize `routes` however you want, of course, after they've been initially automatically generated.

```python
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
```

