import sys
import os

import pytest
from tornado.web import URLSpec

from .utils import handle_import_error

try:
    sys.path.append('.')
    from tornado_json.api_doc_gen import _get_tuple_from_route
    from tornado_json.api_doc_gen import get_api_docs
    from tornado_json.api_doc_gen import _get_notes
    from tornado_json.routes import get_routes
    sys.path.append("demos/helloworld")
    import helloworld
except ImportError as err:
    handle_import_error(err)


def test__get_tuple_from_route():
    """Test tornado_json.api_doc_gen._get_tuple_from_route"""

    class handler_class(object):
        def post(self):
            pass

        def get(self, pk):
            pass

        def delete(self, pk):
            pass

    pattern = r"/$"
    expected_output = (pattern, handler_class, ['post'])

    # Test 2-tuple
    assert _get_tuple_from_route((pattern, handler_class)) == expected_output
    # Test 3-tuple (with the extra arg as kwarg(s)
    assert _get_tuple_from_route((pattern, handler_class, None)) == expected_output
    # Test URLSpec
    assert _get_tuple_from_route(URLSpec(pattern, handler_class)) == expected_output

    pattern = r"/(?P<pk>[a-zA-Z0-9_\\-]+)/$"
    expected_output = (pattern, handler_class, ['get', 'delete'])
    # Test 2-tuple
    assert _get_tuple_from_route((pattern, handler_class)) == expected_output
    # Test 3-tuple (with the extra arg as kwarg(s)
    assert _get_tuple_from_route((pattern, handler_class, None)) == expected_output
    # Test URLSpec
    assert _get_tuple_from_route(URLSpec(pattern, handler_class)) == expected_output

    # Test invalid type
    with pytest.raises(TypeError):
        _get_tuple_from_route([])
    # Test malformed tuple (i.e., smaller length than 2)
    with pytest.raises(AssertionError):
        _get_tuple_from_route(("foobar",))



def test__get_api_docs():
    relative_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(relative_dir, "helloworld_API_documentation.md")
    HELLOWORLD_DOC = open(filepath).read()

    assert get_api_docs(get_routes(helloworld)) == HELLOWORLD_DOC


def test___get_notes():
    def test_no_doc():
        pass

    assert _get_notes(test_no_doc) is None

    def test_doc():
        """This is not a drill"""
        pass

    assert test_doc.__doc__ in _get_notes(test_doc)
