import sys
import pytest
from jsonschema import ValidationError

try:
    sys.path.append('.')
    from tornado_json import routes
    from tornado_json import utils
    sys.path.append('demos/helloworld')
    import helloworld
except ImportError:
    print("Please run `py.test` from the root project directory")
    exit(1)


class SuccessException(Exception):

    """Great success!"""


class MockRequestHandler(object):

    class Request(object):
        body = "{\"I am a\": \"JSON object\"}"

    request = Request()

    def fail(message):
        raise APIError(message)

    def success(self, message):
        raise SuccessException


class TestTornadoJSONBase(object):

    """Base class for all tornado_json test classes"""


class TestRoutes(TestTornadoJSONBase):

    """Tests the routes module"""

    def test_get_routes(self):
        """Tests routes.get_routes"""
        assert routes.get_routes(
            helloworld) == [("/api/helloworld",
                             helloworld.api.HelloWorldHandler)]

    def test_gen_submodule_names(self):
        """Tests routes.gen_submodule_names"""
        assert list(routes.gen_submodule_names(helloworld)
                    ) == ['helloworld.api']

    def test_get_module_routes(self):
        """Tests routes.get_module_routes"""
        assert routes.get_module_routes(
            'helloworld.api') == [("/api/helloworld",
                                   helloworld.api.HelloWorldHandler)]


class TestUtils(TestTornadoJSONBase):

    """Tests the utils module"""

    def test_api_assert(self):
        """Test utils.api_assert"""
        with pytest.raises(utils.APIError):
            utils.api_assert(False, 400)

        utils.api_assert(True, 400)

    class TerribleHandler(MockRequestHandler):

        """This 'handler' is used in test_io_schema"""

        apid = {
            "get": {
                "input_schema": "This doesn't matter because GET request",
                "output_schema": {
                    "type": "number",
                },
            },
            "post": {
                "input_schema": {
                    "type": "number",
                },
                "output_schema": {
                    "type": "number",
                },
            },
        }

        @utils.io_schema
        def get(self, body):
            return "I am not the handler you are looking for."

        @utils.io_schema
        def post(self, body):
            return "Fission mailed."

    class ReasonableHandler(MockRequestHandler):

        """This 'handler' is used in test_io_schema"""

        apid = {
            "get": {
                "input_schema": None,
                "output_schema": {
                    "type": "string",
                },
            },
            "post": {
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "I am a": {"type": "string"},
                    },
                    "required": ["I am a"],
                },
                "output_schema": {
                    "type": "string",
                },
            },
        }

        @utils.io_schema
        def get(self, body):
            return "I am the handler you are looking for."

        @utils.io_schema
        def post(self, body):
            return "Mail received."

    def test_io_schema(self):
        """Tests the utils.io_schema decorator"""
        th = self.TerribleHandler()
        rh = self.ReasonableHandler()

        # Expect a TypeError to be raised because of invalid output
        with pytest.raises(TypeError):
            th.get()

        # Expect a validation error because of invalid input
        with pytest.raises(ValidationError):
            th.post()

        # Both of these should succeed as the body matches the schema
        with pytest.raises(SuccessException):
            rh.get()
        with pytest.raises(SuccessException):
            rh.post()
