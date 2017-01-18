__author__ = 'ilya'

import importlib
import inspect
from itertools import chain


from tornado_json.routes import gen_submodule_names


def get_routes(package, base="api"):
    """
    This will walk ``pacakge`` and generate routes from any and all
    ``Api handler`` and ``ViewHandler`` subclasses it finds.

    :type package: package
    :param package: Package containing RequestHandlers
    :type base: str
    :param base: A base path for all future urls. Defaults to "api".
    :returns: List of routes for all submodules of ``package``
    :rtype: [(url, RequestHandler), ... ]
    """

    return list(chain(*[get_module_routes(modname, base) for modname
                        in gen_submodule_names(package)]))


def into_path(cls_name, module_name):

    """
    This function constructs appropriate path for api.
    Classname here is an actual class name minus the 'Handler' part, if present.
    If Classname matches module name and plural:
        url returned will be '%modulename%'
    If Classname matches module name and singular:
        url returned will be '%modulename%/(.*)' (i.e query for a single object by id)
    If Classname does not match the module name, regardless of it's form:
        url returned will be '%modulename%/%classname%'. This might represent an action on list level.
    :param cls_name: Name of the handler
    :param module_name: Name of the module containing the handler
    :return: a url path for given handler.
    """

    name = cls_name.split('Handler')[0]

    if name == 'Base':
        return None
    if name[-1] == 's' and name.lower() == module_name.lower():
        return module_name.lower()
    elif name[-1] != 's' and (name+'s').lower() == module_name:
        return r"%s/(.*)" % module_name.lower()
    else:
        return r"%s/%s" % (module_name.lower(), name.lower())


def get_module_routes(module_name, base):
    """
    Constructs a full url path with a link to a handler for a given module.
    I.E, if module is handlers.images and contains ImageHandler and ImagesHandler
    it will produce two tuples
    (r'/%base%/images', ImagesHandler)
    (r'/%base%/images/(.*)', ImageHandler)

    :type module_name: str
    :param module_name: a name of module to construct urls for.
    :type base: str
    :param base: Base path for all urls constructed.
    :return: a list of urls linked to handlers, ready for tornado Application.
    """

    routes = []
    module = importlib.import_module(module_name)

    for cls_name, cls in inspect.getmembers(module, inspect.isclass):
        route = r"/%s/%s" % (base, into_path(cls_name, module_name.split('.')[1]))
        if 'None' not in route:
            routes.append((route, cls))

    return routes