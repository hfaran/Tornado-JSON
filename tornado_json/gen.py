import inspect

from tornado import gen


def coroutine(func):
    """Tornado-JSON compatible wrapper for ``tornado.gen.coroutine``

    Annotates original argspec.args of ``func`` as attribute ``__argspec_args``
    """
    wrapper = gen.coroutine(func)
    wrapper.__argspec_args = inspect.getfullargspec(func).args
    return wrapper
