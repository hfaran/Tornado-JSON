import logging
import json


def api_doc_gen(routes):
    """
    Generates GitHub Markdown formatted API documentation using
    provided information from `api_documentation` class-variable
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
                url,
                "\n\n".join(
                    [
"""## {0}
### Input
```
{1}
```
### Output
```
{2}
```

{3}
""".format(
                method.upper(),
                json.dumps(rh.api_documentation[method]
                           ["input_schema"], indent=4),
                json.dumps(rh.api_documentation[method]
                           ["output_schema"], indent=4),
                rh.api_documentation[method]["doc"],
            ) for method in rh.api_documentation.keys()
                    ]
                )
            )
            documentation.append(route_doc)
        # If a RequestHandler does not yet have an api_documentation variable
        #  just ignore it and continue
        except AttributeError as e:
            logging.info(str(e))
            continue

    # Documentation is written to the root folder
    with open("API_Documentation.md", "w+") as f:
        f.write("\n\n\n".join(documentation))
