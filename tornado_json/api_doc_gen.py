import logging
import json


def api_doc_gen(routes):
    """
    Generates GitHub Markdown formatted API documentation using
    provided information from `apid` class-variable
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
# `{0}`

    Content-Type: application/json

{1}
""".format(
                url,
                "\n\n".join(
                    [
"""## {0}
### Input Schema
```json
{1}
```
{4}
### Output Schema
```json
{2}
```
{5}

{3}
""".format(
                method.upper(),
                json.dumps(rh.apid[method]
                           ["input_schema"], indent=4),
                json.dumps(rh.apid[method]
                           ["output_schema"], indent=4),
                rh.apid[method]["doc"],
"""
### Input Example
```json
{}
```
""".format(json.dumps(rh.apid[method]["input_example"], indent=4))
                if rh.apid[method].get("input_example") else "",
"""
### Output Example
```json
{}
```
""".format(json.dumps(rh.apid[method]["output_example"], indent=4))
                if rh.apid[method].get("output_example") else "",
            ) for method in list(rh.apid.keys())
                    ]
                )
            )
            documentation.append(route_doc)
        # If a RequestHandler does not yet have an apid variable
        #  just ignore it and continue
        except AttributeError as e:
            logging.info(str(e))
            continue

    # Documentation is written to the root folder
    with open("API_Documentation.md", "w+") as f:
        f.write(
            "**This documentation is automatically generated.**\n\n" +
            "**Output schemas only represent `data` and not the full output; see output examples and the JSend specification.**\n" +
            "\n\n\n".join(documentation)
        )
