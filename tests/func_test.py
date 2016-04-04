import json
import sys

from jsonschema.validators import Draft4Validator, create
from tornado.testing import AsyncHTTPTestCase

from .utils import handle_import_error

try:
    sys.path.append('.')
    from tornado_json import routes
    from tornado_json import schema
    from tornado_json import application
    from tornado_json import requesthandlers
    sys.path.append('demos/helloworld')
    import helloworld
except ImportError as err:
    handle_import_error(err)


def jd(obj):
    return json.dumps(obj)


def jl(s):
    return json.loads(s.decode("utf-8"))


class DummyView(requesthandlers.ViewHandler):
    """Dummy ViewHandler for coverage"""
    def delete(self):
        # Reference db_conn to test for AttributeError
        self.db_conn

meta_schema = Draft4Validator.META_SCHEMA.copy()
meta_schema['definitions']["simpleTypes"]['enum'].append('int')

default_types = Draft4Validator.DEFAULT_TYPES.copy()
default_types['int'] = int


ExtendedDraft4Validator = create(meta_schema,
                                 Draft4Validator.VALIDATORS,
                                 default_types=default_types)


class PeopleHandler(requesthandlers.APIHandler):
    """Example handler with input schema validation that uses custom Validator.
    """
    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "name": {'type': "string"},
                "age": {'type': "int"},
            },
            'required': ['name', 'age'],
        },
        validator_cls=ExtendedDraft4Validator
    )
    def post(self):
        return self.body['name']


def get_countries():
    return ['Brazil', 'Argentina']


class MemberHandler(requesthandlers.APIHandler):
    """Example handler with input schema validation that uses SchemaCallback
    """
    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "name": {'type': "string"},
                "country": {'enum': schema.SchemaCallback(get_countries)}
            },
            "required": ['name', 'country'],
        }
    )
    def post(self):
        return self.body['name']


class DBTestHandler(requesthandlers.APIHandler):
    """APIHandler for testing db_conn"""
    def get(self):
        # Set application.db_conn to test if db_conn BaseHandler
        #   property works
        self.application.db_conn = {"data": "Nothing to see here."}
        self.success(self.db_conn.get("data"))


class ExplodingHandler(requesthandlers.APIHandler):

    @schema.validate(**{
        "input_schema": None,
        "output_schema": {
            "type": "number",
        }
    })
    def get(self):
        """This handler is used for testing purposes and is explosive."""
        return "I am not the handler you are looking for."

    @schema.validate(**{
        "input_schema": {
            "type": "number",
        },
        "output_schema": {
            "type": "number",
        }
    })
    def post(self):
        """This handler is used for testing purposes and is explosive."""
        return "Fission mailed."


class NotFoundHandler(requesthandlers.APIHandler):

    @schema.validate(**{
        "output_schema": {
            "type": "number",
        },
        "on_empty_404": True
    })
    def get(self):
        """This handler is used for testing empty output."""
        return 0

    @schema.validate(**{
        "input_schema": {
            "type": "number",
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "required": ["name", ]
        }
    })
    def post(self):
        """This handler is used for testing empty json output."""
        return {}


class APIFunctionalTest(AsyncHTTPTestCase):

    def get_app(self):
        rts = routes.get_routes(helloworld)
        rts += [
            ("/api/member", PeopleHandler),
            ("/api/people", PeopleHandler),
            ("/api/explodinghandler", ExplodingHandler),
            ("/api/notfoundhandler", NotFoundHandler),
            ("/views/someview", DummyView),
            ("/api/dbtest", DBTestHandler),
        ]
        return application.Application(
            routes=rts,
            settings={"debug": True},
            db_conn=None
        )

    def test_post_schemacallback(self):
        """ Test if SchemaCallback will be evalued
        """
        r = self.fetch(
            "/api/people",
            method="POST",
            body=jd({
                'name': "Paulo",
            })
        )
        self.assertEqual(r.code, 400)

    def test_post_custom_validator_class(self):
        """It should not raise errors because ExtendedDraft4Validator is used,
        so schema type 'int' is allowed. """
        r = self.fetch(
            "/api/member",
            method="POST",
            body=jd({
                'name': "Paulo",
                'age': 29,
            })
        )
        self.assertEqual(r.code, 200)

    def test_synchronous_handler(self):
        r = self.fetch(
            "/api/helloworld"
        )
        self.assertEqual(r.code, 200)
        self.assertEqual(
            jl(r.body)["data"],
            "Hello world!"
        )

    def test_asynchronous_handler(self):
        r = self.fetch(
            "/api/asynchelloworld/name"
        )
        self.assertEqual(r.code, 200)
        self.assertEqual(
            jl(r.body)["data"],
            "Hello (asynchronous) world! My name is name."
        )

    def test_post_request(self):
        r = self.fetch(
            "/api/postit",
            method="POST",
            body=jd({
                "title": "Very Important Post-It Note",
                "body": "Equally important message",
                "index": 0
            })
        )
        self.assertEqual(r.code, 200)
        self.assertEqual(
            jl(r.body)["data"]["message"],
            "Very Important Post-It Note was posted."
        )

    def test_url_pattern_route(self):
        r = self.fetch(
            "/api/greeting/John/Smith"
        )
        self.assertEqual(r.code, 200)
        self.assertEqual(
            jl(r.body)["data"],
            "Greetings, John Smith!"
        )

    def test_write_error(self):
        # Test malformed output
        r = self.fetch(
            "/api/explodinghandler"
        )
        self.assertEqual(r.code, 500)
        self.assertEqual(
            jl(r.body)["status"],
            "error"
        )
        # Test malformed input
        r = self.fetch(
            "/api/explodinghandler",
            method="POST",
            body='"Yup", "this is going to end badly."]'
        )
        self.assertEqual(r.code, 400)
        self.assertEqual(
            jl(r.body)["status"],
            "fail"
        )

    def test_empty_resource(self):
        # Test empty output
        r = self.fetch(
            "/api/notfoundhandler"
        )
        self.assertEqual(r.code, 404)
        self.assertEqual(
            jl(r.body)["status"],
            "fail"
        )
        # Test empty output on_empty_404 is False
        r = self.fetch(
            "/api/notfoundhandler",
            method="POST",
            body="1"
        )
        self.assertEqual(r.code, 500)
        self.assertEqual(
            jl(r.body)["status"],
            "error"
        )

    def test_view_db_conn(self):
        r = self.fetch(
            "/views/someview",
            method="DELETE"
        )
        self.assertEqual(r.code, 500)
        self.assertTrue(
            "No database connection was provided." in r.body.decode("UTF-8")
        )

    def test_db_conn(self):
        r = self.fetch(
            "/api/dbtest",
            method="GET"
        )
        self.assertEqual(r.code, 200)
        print(r.body)
        self.assertEqual(
            jl(r.body)["status"],
            "success"
        )
        self.assertTrue(
            "Nothing to see here." in jl(r.body)["data"]
        )
