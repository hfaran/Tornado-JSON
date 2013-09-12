from tornado.web import HTTPError


class APIError(HTTPError):

    """Equivalent to RequestHandler.HTTPError except for in name"""


def api_assert(condition, *args, **kwargs):
    """Asserts that condition is True, else raises an APIError with the
    provided args and kwargs
    """
    if not condition:
        raise APIError(*args, **kwargs)
