.. tornado_json documentation master file, created by
   sphinx-quickstart on Thu Dec 19 00:44:46 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tornado-JSON
========================================

Tornado-JSON is a small extension of `Tornado <http://www.tornadoweb.org/en/stable/>`__ with the intent providing
the tools necessary to get a JSON API up and running quickly. See
`demos/helloworld/ <https://github.com/hfaran/Tornado-JSON/tree/master/demos/helloworld>`__
for a quick example and the `accompanying
walkthrough <http://tornado-json.readthedocs.org/en/latest/using_tornado_json.html>`__
in the documentation.

Some of the key features the included modules provide:

-  Input and output `JSON Schema <http://json-schema.org/>`__ validation
   by decorating RequestHandlers with ``schema.validate``
-  Automated *route generation* with ``routes.get_routes(package)``
-  *Automated Public API documentation* using schemas and provided
   descriptions
-  Standardized output using the
   `JSend <http://labs.omniti.com/labs/jsend>`__ specification

**Contents**:

.. toctree::
   :maxdepth: 2

   installation
   using_tornado_json
   requesthandler_guidelines
   docgen
   restapi
   changelog
   tornado_json



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
