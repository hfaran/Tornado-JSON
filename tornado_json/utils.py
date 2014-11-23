import types
import pyclbr
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


def is_handler_subclass(cls, classnames=("ViewHandler", "APIHandler")):
    """Determines if ``cls`` is indeed a subclass of ``classnames``

    This function should only be used with ``cls`` from ``pyclbr.readmodule``
    """
    if isinstance(cls, pyclbr.Class):
        return is_handler_subclass(cls.super)
    elif isinstance(cls, list):
        return any(is_handler_subclass(s) for s in cls)
    elif isinstance(cls, str):
        return cls in classnames
    else:
        raise TypeError(
            "Unexpected pyclbr.Class.super type `{}` for class `{}`".format(
                type(cls),
                cls
            )
        )
