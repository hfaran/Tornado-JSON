Changelog
=========

_
---------


1.3.3
~~~~~

* Support Tornado >= 5.0 and Python 3.6


1.3.2
~~~~~

* Recovery release for PyPI (1.3.1 had an incomplete module included accidentally)


1.3.1
~~~~~

* Minor updates with versioning


1.3.0
~~~~~

* Added use_defaults support for schema.validate
* Added support for custom validators
* Bugfix: Fixed api_doc_gen duplicated entries
* Bugfix: Remove pyclbr and use inspect instead for module introspection


1.2.2
~~~~~

* `generate_docs` parameter added to `Application` for optional API documentation generation


1.2.1
~~~~~

* arg_pattern now contains hyphen
* Handle case where server would crash when generating docs for methods with
no docstring
* Add support for tornado==3.x.x gen.coroutine
* Add format_checker kwarg to schema.validate


1.2.0
~~~~~

* Implement ``tornado_json.gen.coroutine``
    * As a fix for `#59 <https://github.com/hfaran/Tornado-JSON/issues/59>`_, a custom wrapper for the ``tornado.gen.coroutine`` wrapper has been implemented. This was necessary as we lose the original argspec through it because the wrapper simply has ``(*args, **kwargs)`` as its signature. Here, we annotate the original argspec as an attribute to the wrapper so it can be referenced later by Tornado-JSON when generating routes.


1.1.0
~~~~~

* Handle routes as ``URLSpec`` and >2-tuple in ``api_doc_gen``
* Refactor ``api_doc_gen``; now has public function ``get_api_doc`` for use


1.0.0
~~~~~

* Compatibility updates for ``tornado>=4.0.0``


v0.41
~~~~~

* Fixed ``JSendMixin`` hanging if auto_finish was disabled


v0.40 - Replace ``apid`` with parameterized ``schema.validate``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The ``apid`` class-variable is no longer used
* Schemas are passed as arguments to ``schema.validate``
* Method docstrings are used in public API documentation, in place of ``apid[method]["doc"]``


v0.31 - On input schema of ``None``, input is presumed to be ``None``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Rather than forcing an input schema of ``None`` with ``GET`` and ``DELETE`` methods, whether input is JSON-decoded or not, is dependent on whether the provided input schema is ``None`` or not. This means that ``get`` and ``delete`` methods can now have request bodies if desired.


v0.30 - URL Annotations
~~~~~~~~~~~~~~~~~~~~~~~

* Added ``__urls__`` and ``__url_names__`` attributes to allow flexible creation of custom URLs that make creating REST APIs etc. easy
* Added a REST API demo as an example for URL annotations
* Added URL annotations documentation
* Refactored and improved route generation in ``routes``


v0.20 - Refactor of ``utils`` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Functions that did not belong in ``utils`` were moved to more relevant modules. This change changes the interface for Tornado-JSON in quite a big way. The following changes were made (that are not backwards compatible).

* ``api_assert`` and ``APIError`` were moved to ``tornado_json.exceptions``
* ``io_schema`` was renamed ``validate`` and moved to ``tornado_json.schema``


v0.14 - Bugfixes thanks to 100% coverage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fixes related to error-writing in ``io_schema`` and ``APIHandler.write_error``


v0.13 - Add asynchronous compatibility to io_schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add asynchronous functionality to io_schema


v0.12 - Python3 support
~~~~~~~~~~~~~~~~~~~~~~~

* Python3.3, in addition to Python2.7, is now supported.


v0.11 - Duplicate route bugfix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Fixed bug where duplicate routes would be created on existence of multiple HTTP methods.


v0.10 - Route generation with URL patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Route generation will now inspect method signatures in ``APIHandler`` and ``ViewHandler`` subclasses, and construct routes with URL patterns based on the signatures. URL patterns match ``[a-zA-Z0-9_]+``.

**Backwards Compatibility**: ``body`` is no longer provided by ``io_schema`` as the sole argument to HTTP methods. Any existing code using ``body`` can now use ``self.body`` to get the same object.


v0.08 - Input and output example fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Add input_example and output_example fields
* status_code 400 on ValidationError
* Exclude delete from input validation
