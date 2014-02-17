import sys
import json
from tornado.testing import AsyncHTTPTestCase

try:
    sys.path.append('.')
    from tornado_json import routes
    from tornado_json import utils
    from tornado_json import jsend
    from tornado_json import application
    sys.path.append('demos/helloworld')
    import helloworld
except ImportError as e:
    print("Please run `py.test` from the root project directory")
    exit(1)


def jd(obj):
    return json.dumps(obj)


def jl(s):
    return json.loads(s.decode("utf-8"))


class APIFunctionalTest(AsyncHTTPTestCase):

    def get_app(self):
        return application.Application(
            routes=routes.get_routes(helloworld),
            settings={},
        )

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
            "/api/asynchelloworld"
        )
        self.assertEqual(r.code, 200)
        self.assertEqual(
            jl(r.body)["data"],
            "Hello (asynchronous) world!"
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
            "/api/greeting/Martian"
        )
        self.assertEqual(r.code, 200)
        self.assertEqual(
            jl(r.body)["data"],
            "Greetings, Martian!"
        )
