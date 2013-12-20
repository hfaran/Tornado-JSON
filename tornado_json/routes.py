import pyclbr
import pkgutil


def get_routes(package):
    """
    This will walk `package` and generates routes from any and all
    `APIHandler` and `ViewHandler` subclasses it finds. If you need to
    customize or remove any routes, you can do so to the list of
    returned routes that this generates.

    :type  package: package
    :param package: The package containing RequestHandlers to generate
        routes from
    :returns: List of routes for all submodules of `package`
    """
    return [get_module_routes(modname) for modname in
            gen_submodule_names(package)]


def gen_submodule_names(package):
    """Walk package and yield names of all submodules

    :type  package: package
    :param package: The package to get submodule names of
    :returns: Iterator that yields names of all submodules of `package`
    """
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=package.__path__,
        prefix=package.__name__ + '.',
            onerror=lambda x: None):
        yield modname


def get_module_routes(
        module_name, custom_routes=None, exclusions=None
):
    """Create and return routes for module_name

    Routes are (url, RequestHandler) tuples

    :returns: list of routes for `module_name` with respect to `exclusions`
        and `custom_routes`. Returned routes are with URLs formatted such
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
    if not custom_routes:
        custom_routes = []
    if not exclusions:
        exclusions = []

    # Generate list of RequestHandler names in custom_routes
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
