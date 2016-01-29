import unittest

from tornado_json.schema import get_object_defaults, NoObjectDefaults, \
    input_schema_clean


class TestSchemaMethods(unittest.TestCase):

    def test_input_schema_clean_ignore_other_types(self):
        self.assertEqual(input_schema_clean('ABC-123', {'type': "string"}),
                         "ABC-123")

    def test_input_schema_clean_no_defaults(self):
        self.assertEqual(input_schema_clean({}, {'type': "object"}),
                         {})

    def test_input_schema_clean(self):
        self.assertEqual(
            input_schema_clean(
                {},
                {
                    'type': "object",
                    'properties': {
                        'published': {
                            'default': True,
                            'type': 'boolean',
                        },
                    }
                }
            ),
            {
                'published': True,
            }
        )

    def test_defaults_basic(self):
        self.assertEqual(
            get_object_defaults({
                'type': 'object',
                'properties': {
                    'title': {"type": 'string'},
                    'published': {"type": 'boolean', "default": True},
                }
            }),
            {
                'published': True,
            }
        )

    def test_defaults_no_defaults(self):
        with self.assertRaises(NoObjectDefaults):
            get_object_defaults({
                'type': 'object',
                'properties': {
                    'title': {"type": 'string'},
                }
            })

    def test_defaults_nested_object_default(self):
        self.assertEqual(
            get_object_defaults({
                'type': 'object',
                'properties': {
                    'title': {"type": 'string'},
                    'published': {"type": 'boolean', "default": True},
                    'driver_license': {
                        'default': {'category': "C"},
                        'type': 'object',
                        'properties': {
                            'category': {
                                "type": "string",
                                "maxLength": 1,
                                "minLength": 1,
                            },
                            'shipping_city': {
                                "type": "string",
                                "default": "Belo Horizonte",
                            },
                        }
                    }
                }
            }),
            {
                'published': True,
                'driver_license': {
                    "category": "C",
                    "shipping_city": "Belo Horizonte",
                }
            }
        )


if __name__ == '__main__':
    unittest.main()
