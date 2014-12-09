import sys

import pytest
from tornado.web import URLSpec

from .utils import handle_import_error

try:
    sys.path.append('.')
    from tornado_json.api_doc_gen import _get_tuple_from_route
except ImportError as err:
    handle_import_error(err)


def test__get_tuple_from_route():
    """Test tornado_json.api_doc_gen._get_tuple_from_route"""
    pattern = r"/$"
    handler_class = object
    expected_output = (pattern, handler_class)

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
