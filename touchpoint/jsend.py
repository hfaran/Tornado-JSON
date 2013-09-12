# Source: http://tornadogists.org/6612013/


class JSendMixin(object):

    """http://labs.omniti.com/labs/jsend

    JSend is a specification that lays down some rules for how JSON
    responses from web servers should be formatted.

    JSend focuses on application-level (as opposed to protocol- or
    transport-level) messaging which makes it ideal for use in
    REST-style applications and APIs.
    """

    def success(self, data):
        """When an API call is successful, the JSend object is used as a simple
        envelope for the results, using the data key.
        """
        self.write({'status': 'success', 'data': data})

    def fail(self, data):
        """There was a problem with the data submitted, or some pre-condition
        of the API call wasn't satisfied.
        """
        self.write({'status': 'fail', 'data': data})

    def error(self, message, data=None, code=None):
        """An error occurred in processing the request, i.e. an exception was
        thrown.
        """
        result = {'status': 'error', 'message': message}
        if data:
            result['data'] = data
        if code:
            result['code'] = code
        self.write(result)
