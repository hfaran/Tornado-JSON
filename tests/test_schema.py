import unittest

from tornado_json.schema import SchemaCallback
from tornado_json.schema import SchemaHelper
from tornado_json.schema import detect_schemacallback
from tornado_json.schema import evaluate_schema_callbacks


class MySchema(SchemaHelper):

    def get_enum_key(self, requesthandler):
        return ['A', 'B']


class MyNestedSchema(SchemaHelper):

    def get_properties_key(self, requesthandler):
        return {
            'myschema': MySchema(),
            'memory_length': {
                'type': "integer",
            }
        }

    def get_title_key(self, requesthandler):
        return "My Nested Schema"


class TestSchemaHelper(unittest.TestCase):

    def test_schemahelper(self):
        sh = MySchema()
        self.assertEqual(
            sh.as_dict(),
            {'enum': ["A", "B"]})

    def test_schemahelper_nested(self):
        sh = MyNestedSchema()
        self.assertEqual(
            sh.as_dict(),
            {
                'title': "My Nested Schema",
                'properties': {
                    'myschema': {
                        'enum': ["A", "B"],
                    },
                    'memory_length': {
                        'type': "integer",
                    },
                },
            })


class TestSchemaCallback(unittest.TestCase):

    def test_evaluate_schema_callbacks(self):

        def get_type():
            return ['object', 'string']

        scb = SchemaCallback(get_type)
        schema = yield evaluate_schema_callbacks({'type': scb})
        self.assertEqual(schema,
                         {'type': ['object', 'string']})

    def test_detect_schemacallback(self):

        def get_users(table, role):
            pks = [1, 10, 100]
            return pks

        scb = SchemaCallback(get_users, "users", role="admin")

        self.assertTrue(detect_schemacallback({
            'properties': {
                'database': {
                    'type': 'object', 'properties': {'database': scb}}}}))

        self.assertFalse(detect_schemacallback({
            'properties': {
                'database': {'type': 'object', 'properties': {}}}}))

    def test_schemacallback(self):

        def get_users(table, role):
            pks = [1, 10, 100]
            return pks

        scb = SchemaCallback(get_users, "users", role="admin")
        result = yield scb()
        self.assertEqual(result, [1, 10, 100])


if __name__ == '__main__':
    unittest.main()
