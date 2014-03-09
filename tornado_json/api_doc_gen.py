import json
import inspect
from jsonschema import validate, ValidationError

from tornado_json.utils import is_method
from tornado_json.constants import HTTP_METHODS
from tornado_json.requesthandlers import APIHandler


def _validate_example(rh, method, example_type):
    """Validates example against schema

    :returns: Formatted example if example exists and validates, otherwise None
    :raises ValidationError: If example does not validate against the schema
    """
    example = getattr(method, example_type + "_example")
    schema = getattr(method, example_type + "_schema")

    if example is None:
        return None

    try:
        validate(example, schema)
    except ValidationError as e:
        raise ValidationError(
            "{}_example for {}.{} could not be validated.\n{}".format(
                example_type, rh.__name__, method.__name__, str(e)
            )
        )

    return json.dumps(example, indent=4)


def _get_rh_methods(rh):
    """Yield all HTTP methods in ``rh`` that are decorated
    with schema.validate"""
    for k, v in vars(rh).items():
        if all([
            k in HTTP_METHODS,
            is_method(v),
            hasattr(v, "input_schema")
        ]):
            yield (k, v)


def api_doc_gen(routes):
    """
    Generates GitHub Markdown formatted API documentation using
    provided schemas in RequestHandler methods and their docstrings.

    :type  routes: [(url, RequestHandler), ...]
    :param routes: List of routes (this is ideally all possible routes of the
        app)
    """
    documentation = []
    # Iterate over routes sorted by url
    for url, rh in sorted(routes, key=lambda a: a[0]):
        # Content-type is hard-coded but ideally should be retrieved;
        #  the hard part is, we don't know what it is without initializing
        #  an instance, so just leave as-is for now

        # BEGIN ROUTE_DOC #
        route_doc = """
# {0}

    Content-Type: application/json

{1}
""".format(
            # Escape markdown literals
            "".join(
                ['\\' + c if c in list("\\`*_{}[]()<>#+-.!:|") else c
                 for c in url]),
            "\n\n".join(
                [
"""## {0}
**Input Schema**
```json
{1}
```
{4}
**Output Schema**
```json
{2}
```
{5}

**Notes**

{3}

""".format(
            method_name.upper(),
            json.dumps(method.input_schema, indent=4),
            json.dumps(method.output_schema, indent=4),
            inspect.getdoc(method),
"""
**Input Example**
```json
{}
```
""".format(_validate_example(rh, method, "input")) if _validate_example(
            rh, method, "input") else "",
"""
**Output Example**
```json
{}
```
""".format(_validate_example(rh, method, "output")) if _validate_example(
            rh, method, "output") else "",
        ) for method_name, method in _get_rh_methods(rh)
                ]
            )
        )
        # END ROUTE_DOC #

        if issubclass(rh, APIHandler):
            documentation.append(route_doc)

    # Documentation is written to the root folder
    with open("API_Documentation.md", "w+") as f:
        f.write(
            "**This documentation is automatically generated.**\n\n" +
            "**Output schemas only represent `data` and not the full output; "
            "see output examples and the JSend specification.**\n" +
            "\n<br>\n<br>\n".join(documentation)
        )
