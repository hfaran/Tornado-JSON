import inspect

from tornado import gen

from tornado_json.constants import TORNADO_MAJOR


def coroutine(func, replace_callback=True):
    """Tornado-JSON compatible wrapper for ``tornado.gen.coroutine``

    Annotates original argspec.args of ``func`` as attribute ``__argspec_args``
    """
    # gen.coroutine in tornado 3.x.x has a different signature from 4.x.x
    if TORNADO_MAJOR == 3:
        wrapper = gen.coroutine(func)
    else:
        wrapper = gen.coroutine(func, replace_callback)
    wrapper.__argspec_args = inspect.getargspec(func).args
    return wrapper
