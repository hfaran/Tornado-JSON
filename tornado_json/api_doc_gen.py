import json
import inspect
import re

try:
    from itertools import imap as map  # PY2
except ImportError:
    pass

import tornado.web
from jsonschema import ValidationError, validate

from tornado_json.utils import extract_method, is_method
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

    return json.dumps(example, indent=4, sort_keys=True)


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


def _get_tuple_from_route(route):
    """Return (pattern, handler_class, methods) tuple from ``route``

    :type route: tuple|tornado.web.URLSpec
    :rtype: tuple
    :raises TypeError: If ``route`` is not a tuple or URLSpec
    """
    if isinstance(route, tuple):
        assert len(route) >= 2
        pattern, handler_class = route[:2]
    elif isinstance(route, tornado.web.URLSpec):
        pattern, handler_class = route.regex.pattern, route.handler_class
    else:
        raise TypeError("Unknown route type '{}'"
                        .format(type(route).__name__))

    methods = []
    route_re = re.compile(pattern)
    route_params = set(list(route_re.groupindex.keys()) + ['self'])
    for http_method in HTTP_METHODS:
        method = getattr(handler_class, http_method, None)
        if method:
            method = extract_method(method)
            method_params = set(getattr(method, "__argspec_args",
                                        inspect.getargspec(method).args))
            if route_params.issubset(method_params) and \
                    method_params.issubset(route_params):
                methods.append(http_method)

    return pattern, handler_class, methods


def _escape_markdown_literals(string):
    """Escape any markdown literals in ``string`` by prepending with \\

    :type string: str
    :rtype: str
    """
    literals = list("\\`*_{}[]()<>#+-.!:|")
    escape = lambda c: '\\' + c if c in literals else c
    return "".join(map(escape, string))


def _cleandoc(doc):
    """Remove uniform indents from ``doc`` lines that are not empty

    :returns: Cleaned ``doc``
    """
    indent_length = lambda s: len(s) - len(s.lstrip(" "))
    not_empty = lambda s: s != ""

    lines = doc.split("\n")
    indent = min(map(indent_length, filter(not_empty, lines)))

    return "\n".join(s[indent:] for s in lines)


def _add_indent(string, indent):
    """Add indent of ``indent`` spaces to ``string.split("\n")[1:]``

    Useful for formatting in strings to already indented blocks
    """
    lines = string.split("\n")
    first, lines = lines[0], lines[1:]
    lines = ["{indent}{s}".format(indent=" " * indent, s=s)
             for s in lines]
    lines = [first] + lines
    return "\n".join(lines)


def _get_example_doc(rh, method, type):
    assert type in ("input", "output")

    example = _validate_example(rh, method, type)
    if not example:
        return ""
    res = """
    **{type} Example**
    ```json
    {example}
    ```
    """.format(
        type=type.capitalize(),
        example=_add_indent(example, 4)
    )
    return _cleandoc(res)


def _get_input_example(rh, method):
    return _get_example_doc(rh, method, "input")


def _get_output_example(rh, method):
    return _get_example_doc(rh, method, "output")


def _get_schema_doc(schema, type):
    res = """
    **{type} Schema**
    ```json
    {schema}
    ```
    """.format(
        schema=_add_indent(json.dumps(schema, indent=4, sort_keys=True), 4),
        type=type.capitalize()
    )
    return _cleandoc(res)


def _get_input_schema_doc(method):
    return _get_schema_doc(method.input_schema, "input")


def _get_output_schema_doc(method):
    return _get_schema_doc(method.output_schema, "output")


def _get_notes(method):
    doc = inspect.getdoc(method)
    if doc is None:
        return None
    res = """
    **Notes**

    {}
    """.format(_add_indent(doc, 4))
    return _cleandoc(res)


def _get_method_doc(rh, method_name, method):
    res = """## {method_name}

    {input_schema}
    {input_example}
    {output_schema}
    {output_example}
    {notes}
    """.format(
        method_name=method_name.upper(),
        input_schema=_get_input_schema_doc(method),
        output_schema=_get_output_schema_doc(method),
        notes=_get_notes(method) or "",
        input_example=_get_input_example(rh, method),
        output_example=_get_output_example(rh, method),
    )
    return _cleandoc("\n".join([l.rstrip() for l in res.splitlines()]))


def _get_rh_doc(rh, methods):
    res = "\n\n".join([_get_method_doc(rh, method_name, method)
                       for method_name, method in _get_rh_methods(rh)
                       if method_name in methods])
    return res


def _get_content_type(rh):
    # XXX: Content-type is hard-coded but ideally should be retrieved;
    #  the hard part is, we don't know what it is without initializing
    #  an instance, so just leave as-is for now
    return "Content-Type: application/json"


def _get_route_doc(url, rh, methods):
    route_doc = """
    # {route_pattern}

        {content_type}

    {rh_doc}
    """.format(
        route_pattern=_escape_markdown_literals(url),
        content_type=_get_content_type(rh),
        rh_doc=_add_indent(_get_rh_doc(rh, methods), 4)
    )
    return _cleandoc(route_doc)


def _write_docs_to_file(documentation):
    # Documentation is written to the root folder
    with open("API_Documentation.md", "w+") as f:
        f.write(documentation)


def get_api_docs(routes):
    """
    Generates GitHub Markdown formatted API documentation using
    provided schemas in RequestHandler methods and their docstrings.

    :type  routes: [(url, RequestHandler), ...]
    :param routes: List of routes (this is ideally all possible routes of the
        app)
    :rtype: str
    :returns: generated GFM-formatted documentation
    """
    routes = map(_get_tuple_from_route, routes)
    documentation = []
    for url, rh, methods in sorted(routes, key=lambda a: a[0]):
        if issubclass(rh, APIHandler):
            documentation.append(_get_route_doc(url, rh, methods))

    documentation = (
        "**This documentation is automatically generated.**\n\n" +
        "**Output schemas only represent `data` and not the full output; " +
        "see output examples and the JSend specification.**\n" +
        "\n<br>\n<br>\n".join(documentation)
    )
    return documentation


def api_doc_gen(routes):
    """Get and write API documentation for ``routes`` to file"""
    documentation = get_api_docs(routes)
    _write_docs_to_file(documentation)
