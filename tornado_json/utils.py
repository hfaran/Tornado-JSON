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
