import pyclbr


def get_module_routes(
        module_name, custom_routes, exclusions
):
    """Create and return routes for module_name

    Routes are (url, RequestHandler) tuples

    :returns: list of routes for module_name with respect to exclusions
        and custom_routes. Returned routes are with URLs formatted such
        that they are /-separated by module/class level and end with the
        lowercase name of the RequestHandler
    :type  module_name: str
    :param module_name: Name of the module to get routes for
    :type  custom_routes: [(str, RequestHandler), ... ]
    :param custom_routes: List of routes that have custom URLs and therefore
        should be automagically generated
    :type  exclusions: [str, str, ...]
    :param exclusions: List of RequestHandler names that routes should not be
        generated for
    """
    custom_routes_s = [c.__name__ for r, c in custom_routes]

    # rhs is a dict of {classname: pyclbr.Class} key, value pairs
    rhs = pyclbr.readmodule(module_name)

    # You better believe this is a list comprehension
    auto_routes = [
        # URL, requesthandler tuple
        (
            "{}/{}".format("/".join(module_name.split(".")), k.lower()),
            getattr(requesthandlers, k)
        )
        # foreach classname, pyclbr.Class in rhs
        for k, v in rhs.iteritems()
        # Only add the pair to auto_routes if:
        #    * the superclass is in the list of supers we want
        #    * the requesthandler isn't already paired in custom_routes
        #    * the requesthandler isn't manually excluded
        if any(
            True for s in v.super if s in ["ViewHandler", "APIHandler"]
        )
        and k not in (custom_routes_s + exclusions)
    ]

    routes = auto_routes + custom_routes
    return routes
