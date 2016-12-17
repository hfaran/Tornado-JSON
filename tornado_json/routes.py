import pkgutil
import importlib
import inspect
from itertools import chain
from functools import reduce

from tornado_json.constants import HTTP_METHODS
from tornado_json.utils import extract_method, is_method, is_handler_subclass


def get_routes(package):
    """
    This will walk ``package`` and generates routes from any and all
    ``APIHandler`` and ``ViewHandler`` subclasses it finds. If you need to
    customize or remove any routes, you can do so to the list of
    returned routes that this generates.

    :type  package: package
    :param package: The package containing RequestHandlers to generate
        routes from
    :returns: List of routes for all submodules of ``package``
    :rtype: [(url, RequestHandler), ... ]
    """
    return list(chain(*[get_module_routes(modname) for modname in
                        gen_submodule_names(package)]))


def gen_submodule_names(package):
    """Walk package and yield names of all submodules

    :type  package: package
    :param package: The package to get submodule names of
    :returns: Iterator that yields names of all submodules of ``package``
    :rtype: Iterator that yields ``str``
    """
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=package.__path__,
        prefix=package.__name__ + '.',
            onerror=lambda x: None):
        yield modname


def get_module_routes(module_name, custom_routes=None, exclusions=None,
                      arg_pattern=r'(?P<{}>[a-zA-Z0-9_\-]+)'):
    """Create and return routes for module_name

    Routes are (url, RequestHandler) tuples

    :returns: list of routes for ``module_name`` with respect to ``exclusions``
        and ``custom_routes``. Returned routes are with URLs formatted such
        that they are forward-slash-separated by module/class level
        and end with the lowercase name of the RequestHandler (it will also
        remove 'handler' from the end of the name of the handler).
        For example, a requesthandler with the name
        ``helloworld.api.HelloWorldHandler`` would be assigned the url
        ``/api/helloworld``.
        Additionally, if a method has extra arguments aside from ``self`` in
        its signature, routes with URL patterns will be generated to
        match ``r"(?P<{}>[a-zA-Z0-9_\-]+)".format(argname)`` for each
        argument. The aforementioned regex will match ONLY values
        with alphanumeric, hyphen and underscore characters. You can provide
        your own pattern by setting a ``arg_pattern`` param.
    :rtype: [(url, RequestHandler), ... ]
    :type  module_name: str
    :param module_name: Name of the module to get routes for
    :type  custom_routes: [(str, RequestHandler), ... ]
    :param custom_routes: List of routes that have custom URLs and therefore
        should be automagically generated
    :type  exclusions: [str, str, ...]
    :param exclusions: List of RequestHandler names that routes should not be
        generated for
    :type  arg_pattern: str
    :param arg_pattern: Default pattern for extra arguments of any method
    """
    def has_method(module, cls_name, method_name):
        return all([
            method_name in vars(getattr(module, cls_name)),
            is_method(reduce(getattr, [module, cls_name, method_name]))
        ])

    def yield_args(module, cls_name, method_name):
        """Get signature of ``module.cls_name.method_name``

        Confession: This function doesn't actually ``yield`` the arguments,
            just returns a list. Trust me, it's better that way.

        :returns: List of arg names from method_name except ``self``
        :rtype: list
        """
        wrapped_method = reduce(getattr, [module, cls_name, method_name])
        method = extract_method(wrapped_method)

        # If using tornado_json.gen.coroutine, original args are annotated...
        argspec_args = getattr(method, "__argspec_args",
                               # otherwise just grab them from the method
                               inspect.getargspec(method).args)

        return [a for a in argspec_args if a not in ["self"]]

    def generate_auto_route(module, module_name, cls_name, method_name, url_name):
        """Generate URL for auto_route

        :rtype: str
        :returns: Constructed URL based on given arguments
        """
        def get_handler_name():
            """Get handler identifier for URL

            For the special case where ``url_name`` is
            ``__self__``, the handler is named a lowercase
            value of its own name with 'handler' removed
            from the ending if give; otherwise, we
            simply use the provided ``url_name``
            """
            if url_name == "__self__":
                if cls_name.lower().endswith('handler'):
                    return cls_name.lower().replace('handler', '', 1)
                return cls_name.lower()
            else:
                return url_name

        def get_arg_route():
            """Get remainder of URL determined by method argspec

            :returns: Remainder of URL which matches `\w+` regex
                with groups named by the method's argument spec.
                If there are no arguments given, returns ``""``.
            :rtype: str
            """
            if yield_args(module, cls_name, method_name):
                return "/{}/?$".format("/".join(
                    [arg_pattern.format(argname) for argname
                     in yield_args(module, cls_name, method_name)]
                ))
            return r"/?"

        return "/{}/{}{}".format(
            "/".join(module_name.split(".")[1:]),
            get_handler_name(),
            get_arg_route()
        )

    if not custom_routes:
        custom_routes = []
    if not exclusions:
        exclusions = []

    # Import module so we can get its request handlers
    module = importlib.import_module(module_name)

    # Generate list of RequestHandler names in custom_routes
    custom_routes_s = [c.__name__ for r, c in custom_routes]

    rhs = {cls_name: cls for (cls_name, cls) in
           inspect.getmembers(module, inspect.isclass)}

    # You better believe this is a list comprehension
    auto_routes = list(chain(*[
        list(set(chain(*[
            # Generate a route for each "name" specified in the
            #   __url_names__ attribute of the handler
            [
                # URL, requesthandler tuple
                (
                    generate_auto_route(
                        module, module_name, cls_name, method_name, url_name
                    ),
                    getattr(module, cls_name)
                ) for url_name in getattr(module, cls_name).__url_names__
                # Add routes for each custom URL specified in the
                #   __urls__ attribute of the handler
            ] + [
                (
                    url,
                    getattr(module, cls_name)
                ) for url in getattr(module, cls_name).__urls__
            ]
            # We create a route for each HTTP method in the handler
            #   so that we catch all possible routes if different
            #   HTTP methods have different argspecs and are expecting
            #   to catch different routes. Any duplicate routes
            #   are removed from the set() comparison.
            for method_name in HTTP_METHODS if has_method(
                module, cls_name, method_name)
        ])))
        # foreach classname, pyclbr.Class in rhs
        for cls_name, cls in rhs.items()
        # Only add the pair to auto_routes if:
        #    * the superclass is in the list of supers we want
        #    * the requesthandler isn't already paired in custom_routes
        #    * the requesthandler isn't manually excluded
        if is_handler_subclass(cls)
        and cls_name not in (custom_routes_s + exclusions)
    ]))

    routes = auto_routes + custom_routes
    return routes
