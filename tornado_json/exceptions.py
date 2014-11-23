from tornado.web import HTTPError


class APIError(HTTPError):
    """Equivalent to ``RequestHandler.HTTPError`` except for in name"""


def api_assert(condition, *args, **kwargs):
    """Assertion to fail with if not ``condition``

    Asserts that ``condition`` is ``True``, else raises an ``APIError``
    with the provided ``args`` and ``kwargs``

    :type  condition: bool
    """
    if not condition:
        raise APIError(*args, **kwargs)
