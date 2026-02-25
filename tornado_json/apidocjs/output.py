try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from json import dump, dumps
from logging import getLogger
from os import makedirs, system
from os.path import exists, join
from textwrap import indent

from tornado_json.constants import HTTP_METHODS
from tornado_json.utils import is_method

from .utils import slugify


logger = getLogger("apidoc")


def format_field_name(schema, original_key, field_name=None, required=[]):
    """Return string declaration for field name.

    :type  schema: dict
    :param schema: the schema
    :type  original_key: str
    :param original_key: original key in schema
    :type  field_name: str
    :param field_name: the field name key
    :type  required: list
    :param required: required fields list
    :rtype: str
    :returns: the formated field name
    """
    if not field_name:
        field_name = original_key

    has_default = 'default' in schema
    not_required = original_key not in required

    if has_default and not_required:
        default = dumps(schema['default'],
                        separators=(',', ':'),
                        sort_keys=True)
        return "[%s=%s]" % (field_name, default)
    elif not_required:
        return "[%s]" % field_name

    return field_name


def format_type(schema, template=None):
    """Return schema as formated type declarative type for api.

    :type  schema: dict
    :param schema: the schema
    :type  template: str
    :param template: template for output
    :rtype: str
    :returns: the formated string
    """

    stype = schema.get('type')
    if isinstance(stype, list):
        for i in stype:
            if i != 'null':
                stype = i
                break

    enum = schema.get('enum', '')
    if enum:
        enum = "=%s" % dumps(enum)[1:-1].replace('", ', '",')

    if template is None:
        template = "%s" + get_array_suffix(schema)

    if stype == 'array' and 'items' in schema:
        return format_type(schema['items'], template)

    elif stype == 'string':
        min_length = schema.get("minLength")
        max_length = schema.get("maxLength")
        if min_length and max_length:
            return "%s{%d..%d}%s" % (template % stype.capitalize(), min_length,
                                     max_length, enum)
        elif min_length:
            return "%s{%d..}%s" % (template % stype.capitalize(), min_length,
                                   enum)
        elif max_length:
            return "%s{..%d}%s" % (template % stype.capitalize(), max_length,
                                   enum)

    elif stype == 'number':
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum and maximum:
            return "%s{%d~%d}%s" % (template % stype.capitalize(), minimum,
                                    maximum, enum)
        elif minimum:
            return "%s{>=%d}%s" % (template % stype.capitalize(), minimum,
                                   enum)
        elif maximum:
            return "%s{<=%d}%s" % (template % stype.capitalize(), maximum,
                                   enum)
    fmt = "%s%s" % (template % stype.capitalize(), enum)
    return fmt


def get_array_suffix(schema):
    """Return the array suffix for format_type.

    It "counts" how many "arrays" a object would be declared as.

    :type  schema: dict
    :param schema: the schema
    :rtype: str
    :returns: the formated suffix: "", "[]", "[][]"
    """
    if schema.get('type') == 'array':
        items = schema.get("items", {})
        return get_array_suffix(items) + '[]'
    return ''


def get_rh_methods(rh):
    """Return all RequestHandler valid HTTP methods."""
    for k, v in sorted(vars(rh).items()):
        if all([
            k in HTTP_METHODS,
            is_method(v),
        ]):
            yield (k, v)


class Notation(object):
    """ Helper class to declare @api notations line. """

    def __init__(self, name, *parts, **kw):
        """
        :type  name: str
        :param name: Param name
        :type  parts: list
        :param parts: Line arguments
        """
        self.name = name
        self.parts = parts
        self.lines = kw.get("lines", [])

    def __str__(self):
        """
        :rtype: string
        :returns: Returns notation line surrounded by new lines.
        """
        lines = ""
        if self.lines:
            lines = "\n"
            lines += "\n".join(self.lines)
            lines = lines.replace("\n", "\n    ")

        s = "\n@%s %s %s\n" % (self.name, " ".join(self.parts), lines)

        return s


def get_method_docstring(method):
    """Return method docstring (If have any doc) left striped.

    :type  method: callable
    :param method: the method to extract doc lines
    :rtype: str
    :returns: docstring
    """
    return (getattr(method, "__doc__", "") or "").lstrip()


def get_input_example_doc(input_example,
                          api_param="apiParamExample",
                          api_param_title="Request-Example"):
    """Return input example Notation.

    :type  input_example: dict
    :param input_example: input example schema
    :type  api_param: str
    :param api_param: Notation param name
    :type  api_param_title: str
    :param api_param_title: Notation param request title
    :rtype: Notation
    :returns: Declared notation
    """
    src = dumps(input_example, indent=4, sort_keys=True)
    doc = Notation(api_param, "{json}", "%s:" % api_param_title, lines=[src])
    return doc


def get_output_example_doc(output_example,
                           api_param="apiSuccessExample",
                           api_param_title="Success-Response"):
    """Return output example Notation.

    :type  output_example: dict
    :param output_example: output example schema
    :type  api_param: str
    :param api_param: Notation param name
    :type  api_param_title: str
    :param api_param_title: Notation param response title
    :rtype: Notation
    :returns: Declared notation
    """
    src = dumps(output_example, indent=4, sort_keys=True)
    doc = Notation(api_param, "{json}", "%s:" % api_param_title,
                   lines=["HTTP/1.1 200 OK",
                          src])
    return doc


def get_output_schema_doc(output_schema, param_name="apiSuccess", preffix=[]):
    """Return output schema Notation.

    :type  output_schema: dict
    :param output_schema: output schema
    :type  param_name: str
    :param param_name: Notation param name
    :type  preffix: list
    :param preffix: previous nested schema keys (for schema nested in objects)
    :rtype: Notation
    :returns: Declared notation
    """
    ostype = output_schema.get("type")
    if ostype not in ('object', 'array'):
        return []

    parts = []

    if ostype in ('object', 'array'):
        schema = get_schema_nested(output_schema)
        required = schema.get("required", [])
        fields = get_schema_fields(schema)
        for k, schema in sorted(fields.items()):
            stype = schema.get('type')
            parts.append(get_schema_notation(k, schema, param_name, preffix,
                                             required))

            if stype == 'object' and 'properties' in schema:
                parts += get_output_schema_doc(schema,
                                               param_name=param_name,
                                               preffix=preffix + [k])

            elif stype == 'array' and 'items' in schema:
                parts += get_output_schema_doc(schema,
                                               param_name=param_name,
                                               preffix=preffix + [k])

    return parts


def get_input_schema_doc(input_schema):
    """Return input schema Notation.

    :type  input_schema: dict
    :param input_schema: output example schema
    :rtype: Notation
    :returns: Declared notation
    """
    return get_output_schema_doc(input_schema, param_name="apiParam")


def get_schema_fields(schema):
    """Return output schema Notation.

    :type  input_schema: dict
    :param input_schema: output example schema
    :rtype: Notation
    :returns: Declared notation
    """
    stype = schema.get("type")
    if stype == 'array':
        sitems = schema.get("items")
        if sitems:
            return get_schema_fields(sitems)

    elif stype == 'object':
        return schema.get('properties', {})

    return {}


def get_schema_nested(schema):
    """Return the this schema or a nested one (if current is array or object).

    :type  schema: dict
    :param schema: the schema
    :rtype: dict
    :returns: the valid schema
    """
    stype = schema.get("type")
    if stype == 'array':
        items = schema.get('items', {})
        itype = items.get('type')
        if itype in ('object', 'array'):
            return get_schema_nested(items)
    elif stype == 'object':
        properties = schema.get('properties', {})
        ptype = properties.get('type')
        if ptype in ('object', 'array'):
            return get_schema_nested(properties)

    return schema


def get_schema_notation(k, schema, param_name, preffix, required):
    """Return the schema Notation.

    :type  k: str
    :param k: the key that the schema resides in parent properties/items dict
    :type  schema: dict
    :param schema: the schema
    :type  preffix: list
    :param preffix: list of previous keys (nested)
    :type  required: list
    :param required: list of required keys from parent properties/items  dict
    :rtype: Notation
    :returns: the schema Notation
    """
    stype = schema.get('type')
    description = schema.get("description")
    if stype == 'object' and description is None:
        description = schema.get("title", "")

    key = k
    if preffix:
        key = ".".join(preffix + [k])

    logger.debug("Adding notation {0}".format(param_name))
    logger.debug("Notation schema {0}".format(schema))

    if 'type' not in schema:
        msg = 'Type not declared on schema {0}'.format(schema)
        logger.error(msg)
        raise Exception(msg)

    p = Notation(
        param_name,
        "{%s}" % format_type(schema),
        format_field_name(schema,
                          k,
                          key,
                          required),
        description or '')

    return p


def get_output_source(apidoc, url, rh_class):
    """Return output source for the chosen url and RequestHandler.

    :type  apidoc: dict
    :param apidoc: apidocjs params
    :type  url: str
    :param url: the url
    :type  rh_class: RequestHandler
    :param rh_class: tornado's RequestHandler class
    :rtype: str
    :returns: the dummy python soruce code
    """
    src = []
    for method_type, method in get_rh_methods(rh_class):
        doc = OrderedDict()
        method_docstring = get_method_docstring(method)
        docparts = method_docstring.split("\n") or ['']
        doc['api'] = ("{%s}" % method_type,
                      url,
                      docparts[0], )
        doc['apiVersion'] = apidoc['version']
        doc['apiName'] = "%s%s" % (method_type.upper(), rh_class.__name__)

        if "@apiGroup" not in method_docstring:
            doc['apiGroup'] = rh_class.__name__

        if getattr(method, 'input_schema', None):
            doc['input_schema'] = get_input_schema_doc(method.input_schema)
            doc['input_schema_apiuse'] = Notation("apiUse",
                                                  "SchemaValidationError")

        if getattr(method, 'input_example', None):
            doc['input_example'] = get_input_example_doc(method.input_example)

        if getattr(method, 'output_schema', None):
            output_schema = {
                'type': 'object',
                'properties': {
                    'data': method.output_schema,
                    'status': {
                        'type': 'string',
                        'enum': ['fail', 'success', 'error'],
                    },
                },
                'required': ['data', 'status']
            }
            doc['output_schema'] = get_output_schema_doc(output_schema)

        if getattr(method, 'output_example', None):
            output_example = {
                "data": method.output_example,
                "status": "success"
            }
            doc['output_example'] = get_output_example_doc(output_example)

        # Inherits InternalServerError declarations from errors.py file
        doc['apiUse'] = "InternalServerError"

        parts = []
        for k, v in doc.items():
            if isinstance(v, Notation):
                p = v
            elif isinstance(v, str):
                p = Notation(k, v)
            elif isinstance(v, list):
                if any([isinstance(i, Notation) for i in v]):
                    lines = [str(i) for i in v]
                    p = "".join(lines)
                else:
                    p = ''
            else:
                p = Notation(k, *v)

            parts.append(str(p))

        doc = "\n".join(parts)
        spaces = " " * 8
        doc = indent(doc, spaces)
        pysrc = generate_py_def(method_type,
                                spaces + method_docstring,
                                doc)

        src.append(pysrc)

    src = "\n".join(src)
    return src


def generate_py_def(func_name, docstring, initial_docstring=""):
    """Return dummy python source containing one function with docstring.

    :type  func_name: str
    :param func_name: function name
    :type  docstring: str
    :param docstring: docstring text (not indented)
    :type  initial_docstring: str
    :param initial_docstring: initial docstring
    :rtype: str
    :returns: the python source code
    """
    src = '''
def %s():
    """
%s
%s
    """
    pass
''' % (func_name, docstring, initial_docstring)

    lines = [line.rstrip() for line in src.split("\n")]
    src = '\n'.join(lines)

    return src


def generate_errors_file():
    """Write file declaring @apiError notations.
    """
    src = []

    src.append(generate_py_def("schema_validation_error", """
@apiDefine SchemaValidationError
@apiError SchemaValidationError One schema field did not validate
@apiErrorExample {json} SchemaValidationError-Response:
    HTTP/1.1 400 Bad Request
    {
      "data": "TRACEBACK FROM SERVER",
      "status": "fail"
    }
"""))

    src.append(generate_py_def("internal_server_error", """
@apiDefine InternalServerError
@apiError (Error 5xx) InternalServerError Return data for any internal
    server error
@apiErrorExample {json} InternalServerError-Response:
    HTTP/1.1 500 Internal Server Error
    {
      "status": "error",
      "code": 500,
      "message": "Internal Server Error"
    }
"""))

    src = "\n".join(src)
    return src


def generate_apidoc_skeleton(routes,
                             content_output_path="apidocjs_input",
                             doc_output_path="doc", **kw):
    """Generate apidoc skeleton.

    :type  routes: iterable
    :param routes: tornado's application routes
    :type  content_output_path: str
    :param content_output_path: output path for generated dummy python code
    :type  doc_output_path: str
    :param doc_output_path: destination directory
    """
    apidoc = {
        'name': "My project",
        'title': "My Tornado-JSON based project",
        'version': '0.0.1',
    }
    apidoc.update(kw)
    output_path = join(content_output_path, apidoc['version'])

    if not exists(output_path):
        makedirs(output_path)

    open(join(output_path, 'errors.py'), 'w').write(generate_errors_file())

    dump(apidoc,
         open(join(content_output_path, 'apidoc.json'), 'w'),
         indent=4,
         sort_keys=True)

    for url, rh in routes:
        part = slugify(url)
        fname = "%s_%s.py" % (part, rh.__name__)
        fname = fname.lower()
        fpath = join(output_path, fname)
        src = get_output_source(apidoc, url, rh)
        open(fpath, 'w').write(src)

    system("apidoc -i %s -o %s --verbose --line-ending=LF" %
           (content_output_path, doc_output_path))

    return True
