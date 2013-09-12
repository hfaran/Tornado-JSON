from tornado.web import RequestHandler

from touchpoint.jsend import JSendMixin
from touchpoint.utils import APIError


class BaseHandler(RequestHandler):

    @property
    def db_conn(self):
        return self.application.db_conn


class ViewHandler(BaseHandler):

    def initialize(self):
        self.set_header("Content-Type", "text/html")


class APIHandler(BaseHandler, JSendMixin):

    """RequestHandler for API calls

    * Sets header as application/json
    * Provides custom write_error that writes error back as JSON rather than
    as the standard HTML template
    """

    def initialize(self):
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code, **kwargs):
        """Override of RequestHandler.write_error

        * Call `error()` or `fail()` from JSendMixin depending on which
        exception was raised with provided reason and status code.
        """
        self.clear()

        # If exc_info is not in kwargs, something is very fubar
        if not "exc_info" in kwargs.keys():
            logging.error("exc_info not provided")
            self.set_status(500)
            self.error(message="Internal Server Error", code=500)
            self.finish()

        self.set_status(status_code)

        # Any APIError exceptions raised will result in a JSend fail written
        # back with the log_message as data. Hence, log_message should NEVER
        # expose internals.
        # All other exceptions result in a JSend error being written back,
        # with log_message only written if debug mode is enabled
        exception = kwargs["exc_info"][1]
        if isinstance(exception, APIError):
            self.fail(exception.log_message)
        else:
            self.error(message=self._reason,
                       data=exception.log_message if self.settings.get(
                           "debug") else None,
                       code=status_code)
        self.finish()
