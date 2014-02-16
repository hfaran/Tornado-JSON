.. contents::
   :depth: 3
..

Tornado-JSON
============

|Build Status| |PyPI version| |Coverage Status| |Stories in Ready|

Overview
--------

Tornado-JSON is a small extension of Tornado with the intent providing
the tools necessary to get a JSON API up and running quickly. See
`demos/helloworld/ <https://github.com/hfaran/Tornado-JSON/tree/master/demos/helloworld>`__
for a quick example and the `accompanying
walkthrough <http://tornado-json.readthedocs.org/en/latest/using_tornado_json.html>`__
in the documentation.

Some of the key features the included modules provide:

-  Input and output `JSON Schema <http://json-schema.org/>`__ validation
   by decorating RequestHandlers
-  Automated *route generation* with ``routes.get_routes(package)``
-  *Automated Public API documentation* using schemas and provided
   descriptions
-  Standardized output using the
   `JSend <http://labs.omniti.com/labs/jsend>`__ specification

`Read the Docs for documentation! <http://tornado-json.readthedocs.org/en/latest/index.html#>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

\ *Warning: Tornado-JSON is still very much a work in progress. No
guarantees on backwards-compatibility made, however, I try not to do
that since, as a user, I hate breaking it at least as much as you. That
being said, use it at your own risk.*\

Dependencies
============

*Python2.7 and Python3.3 are supported.*

These dependencies can be satisfied by running
``pip install -r requirements.txt``

-  tornado
-  jsonschema


.. |Build Status| image:: https://travis-ci.org/hfaran/Tornado-JSON.png?branch=master
   :target: https://travis-ci.org/hfaran/Tornado-JSON
.. |PyPI version| image:: https://badge.fury.io/py/Tornado-JSON.png
   :target: http://badge.fury.io/py/Tornado-JSON
.. |Coverage Status| image:: https://coveralls.io/repos/hfaran/Tornado-JSON/badge.png?branch=master
   :target: https://coveralls.io/r/hfaran/Tornado-JSON?branch=master
.. |Stories in Ready| image:: https://badge.waffle.io/hfaran/Tornado-JSON.png?label=ready
   :target: http://waffle.io/hfaran/Tornado-JSON
