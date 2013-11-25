import pyclbr

from touchpoint.signup import requesthandlers
from touchpoint.requesthandlers import BaseHandler


def get_routes():
    """Create and return all routes for signup

    Routes are (url, RequestHandler) tuples

    :returns: list of routes for signup
    """
    # Any routes which are not to be named as the lowercase
    #  name of their respective requesthandler should be entered here
    custom_routes = [(r"/", requesthandlers.PublicHome)]
    custom_routes_s = [c.__name__ for r, c in custom_routes]
    # Exclude any requesthandlers by name (string) here
    exclusions = []  # ex: ["PublicHome"]

    # rhs is a dict of {classname: pyclbr.Class} key, value pairs
    rhs = pyclbr.readmodule("touchpoint.signup.requesthandlers")

    # You better believe this is a list comprehension
    auto_routes = [
        # URL, requesthandler tuple
        (
            "/{}".format(k.lower()),
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
