import logging
import json
from jsonschema import validate, ValidationError


def _validate_example(rh, method, example_type):
    """Validates example against schema

    :returns: Formatted example if example exists and validates, otherwise None
    :raises ValidationError: If example does not validate against the schema
    """
    if not rh.apid[method].get(example_type + "_example"):
        return None
    else:
        try:
            validate(rh.apid[method][example_type + "_example"], rh.apid[method][example_type + "_schema"])
        except ValidationError as e:
            raise ValidationError("{}_example for {}.{} could not be validated.\n{}".format(
                example_type, rh.__name__, method, str(e)
            ))

    return json.dumps(rh.apid[method][example_type + "_example"], indent=4)


def api_doc_gen(routes):
    """
    Generates GitHub Markdown formatted API documentation using
    provided information from ``apid`` class-variable
    in each handler that provides one.

    :type  routes: [(url, RequestHandler), ...]
    :param routes: List of routes (this is ideally all possible routes of the
        app)
    """
    documentation = []
    # Iterate over routes sorted by url
    for url, rh in sorted(routes, key=lambda a: a[0]):
        try:
            # Content-type is hard-coded but ideally should be retrieved;
            #  the hard part is, we don't know what it is without initializing
            #  an instance, so just leave as-is for now
            route_doc = """
# {0}

    Content-Type: application/json

{1}
""".format(
                "".join(['\\' + c if c in list("\\`*_{}[]()<>#+-.!:|") else c for c in url]),  # Escape markdown literals
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
                method.upper(),
                json.dumps(rh.apid[method]
                           ["input_schema"], indent=4),
                json.dumps(rh.apid[method]
                           ["output_schema"], indent=4),
                rh.apid[method]["doc"],
"""
**Input Example**
```json
{}
```
""".format(_validate_example(rh, method, "input")) if _validate_example(rh, method, "input") else "",
"""
**Output Example**
```json
{}
```
""".format(_validate_example(rh, method, "output")) if _validate_example(rh, method, "output") else "",
            ) for method in list(rh.apid.keys())
                    ]
                )
            )
            documentation.append(route_doc)
        # If a RequestHandler does not yet have an apid variable
        #  just ignore it and continue
        except AttributeError as e:
            logging.debug(str(e))

    # Documentation is written to the root folder
    with open("API_Documentation.md", "w+") as f:
        f.write(
            "**This documentation is automatically generated.**\n\n" +
            "**Output schemas only represent `data` and not the full output; see output examples and the JSend specification.**\n" +
            "\n<br>\n<br>\n".join(documentation)
        )
