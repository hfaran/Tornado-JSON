import inspect

from tornado import gen


def coroutine(func, replace_callback=True):
    """Tornado-JSON compatible wrapper for ``tornado.gen.coroutine``

    Annotates original argspec.args of ``func`` as attribute ``__argspec_args``
    """
    wrapper = gen.coroutine(func, replace_callback)
    wrapper.__argspec_args = inspect.getargspec(func).args
    return wrapper
