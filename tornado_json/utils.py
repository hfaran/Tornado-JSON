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


def ensure_endswith(s, sub):
    """Ensures that ``s`` ends with ``sub``

    :type s: str
    :type sub: str

    Strategy:
    Start checking if ``s`` ends with characters from ``sub`` in reverse.
    If a match is found for a character from ``sub``, we keep checking
    to ensure that a substring of ``sub`` exists at the end of ``s``, such
    that ``s.endswith(sub[:n])`` is True where ``1<=n<len(sub)``. As we check
    we strip this character from ``s``. If the above condition is not
    satisfied for the entirety of the loop; give up and suffix ``sub``
    entirely to ``s``; otherwise, we strip off the substring of ``sub``
    that exists at the end of ``s`` and then append the entirety of ``sub``
    to it and return.

    >>> ensure_endswith("/api/?", "/?")
    '/api/?'
    >>> ensure_endswith("/api?", "/?")
    '/api?/?'
    >>> ensure_endswith("/api/", "/?")
    '/api/?'
    >>> ensure_endswith("/api/foobar", "/?")
    '/api/foobar/?'
    """
    new_s = s
    match_started = False
    for c in reversed(sub):
        if new_s.endswith(c):
            match_started = True
            new_s = new_s[:-1]
        else:
            if match_started is True:
                new_s = s
                break
    return new_s + sub
