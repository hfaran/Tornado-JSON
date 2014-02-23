Creating a REST API Using URL Annotations
=========================================

You may have noticed that the automatic URL generation
is meant to be quick and easy-to-use for simple cases (creating an
API in 15 minutes kind of thing).

It is more powerful though, however, as you can customize it
to get the URLs for RequestHandlers how you want without
having to make additions to output from ``routes.get_routes``
yourself. This is done through the use of "URL annotations".
``APIHandler`` and ``ViewHandler`` have two "magic" attributes
(``__urls__`` and ``__url_names__``) that allow you to define custom routes right in the handler
body. See relevant documentation in the
`REST API <https://github.com/hfaran/Tornado-JSON/blob/master/demos/rest_api/cars/api/__init__.py>`__
example in the demos.
