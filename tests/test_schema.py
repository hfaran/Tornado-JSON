import unittest

from tornado_json.schema import get_object_defaults
from tornado_json.schema import input_schema_clean
from tornado_json.schema import NoObjectDefaults


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
                {'publishing': {'publish_date': '2012-12-12'}},
                {
                    'type': "object",
                    'properties': {
                        'publishing': {
                            'type': 'object',
                            'properties': {
                                'publish_date': {
                                    'type': 'string',
                                },

                                'published': {
                                    'default': True,
                                    'type': 'boolean',
                                },
                            },
                        },
                    }
                }
            ),
            {
                'publishing': {
                    'published': True,
                    'publish_date': '2012-12-12',
                },
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
                    'address': {
                        "type": 'object',
                        'properties': {
                            'street': {
                                'type': 'string',
                            }
                        }
                    },
                }
            })

    def test_defaults_nested_object_default(self):
        self.assertEqual(
            get_object_defaults({
                'type': 'object',
                'properties': {
                    'title': {"type": 'string'},
                    'published': {"type": 'boolean', "default": True},
                    'address': {
                        'type': 'object',
                        'properties': {
                            'country': {
                                'type': 'string',
                                'default': "Brazil",
                            },
                        },
                    },
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
                'address': {
                    'country': "Brazil",
                },
                'driver_license': {
                    "category": "C",
                    "shipping_city": "Belo Horizonte",
                }
            }
        )


if __name__ == '__main__':
    unittest.main()
