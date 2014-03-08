import types

from functools import wraps


def container(dec):
    """Meta-decorator (for decorating decorators)

    Keeps around original decorated function as a property ``orig_func``

    :param dec: Decorator to decorate
    :type  dec: function
    :returns: Decorated decorator
    """
    # Credits: http://stackoverflow.com/a/1167248/1798683
    @wraps(dec)
    def meta_decorator(f):
        decorator = dec(f)
        decorator.orig_func = f
        return decorator
    return meta_decorator


def extract_method(wrapped_method):
    """Gets original method if wrapped_method was decorated

    :rtype: any([types.FunctionType, types.MethodType])
    """
    # If method was decorated with validate, the original method
    #   is available as orig_func thanks to our container decorator
    return wrapped_method.orig_func if \
        hasattr(wrapped_method, "orig_func") else wrapped_method


def is_method(method):
    method = extract_method(method)
    # Can be either a method or a function
    return type(method) in [types.MethodType, types.FunctionType]
