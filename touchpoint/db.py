import torndb
import dataset
import time

from tornado.options import define, options


define("mysql_host", default="127.0.0.1:3306")
define("mysql_database", default="touchpoint")
define("mysql_user", default="touchpt-dev")
define("mysql_password", default="pooltable")


class Connection(object):

    def __init__(self):
        """
        Create torndb and dataset connections to database
            - torndb should be used for custom SQL queries
            - dataset is encouraged for simple find and insert queries
        """
        self.__db_torndb = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password,
        )
        self.__db_dataset = dataset.connect(
            "mysql://{}:{}@{}/{}".format(
                options.mysql_user,
                options.mysql_password,
                options.mysql_host,
                options.mysql_database,
            )
        )

    def generic_query(self, method, query, parameters=None, force=False):
        """torndb.Connection.method(query, *parameters)

        This method attempts to force proper parameterization of SQL
        queries to prevent SQL injection
            - Any queries to the db MUST be made with this method
            - This method does not yet support kwparameters (if needed,
                will add)

        :type  method: str
        :param method: The name of the torndb.Connection method you wish to
            call.
        :type  query: str
        :param query: The query you wish to call `method` on
        :type  parameters: list
        :param parameters: The parameters to inserted into a query if it is
            parameterized.
        :type  force: bool
        :param force: If set to `True`, overrides the check and parameterizes
            anyway.
        :returns: The result of the query
        """
        _method = getattr(self.__db_torndb, method)
        parameterized = any(c in query for c in ["%", "{"]) and not force

        if parameterized:
            assert parameters, "Expected parameters for parameterized query"
            return _method(query, *parameters)
        else:
            return _method(query)

    def get_email_suffixes(self):
        """:returns: list of email suffixes"""
        return self.generic_query("query", "SELECT * FROM email_suffixes")

    def get_all_emails(self):
        """:returns: all email addresses in DB"""
        return self.generic_query("query", "SELECT email FROM persons")

    def create_person(self, kwargs):
        """Writes a new person to the DB

        :type  kwargs: dict
        :param kwargs: Dictionary of required details to insert into DB
        """
        # Parameterized query left here as an example
        # return self.generic_query(
        #     "execute",
        #     ("INSERT INTO persons (first, last, email, "
        #      "salt, password, karma, time)"
        #      " VALUES (%s,%s,%s,%s,%s,%s,%s)"),
        #     [kwargs["first"], kwargs["last"],
        #      kwargs["email"], kwargs["salt"],
        #      kwargs["password"], 0, int(time.time())]
        # )

        # Here we use dataset to execute the same query as above
        table = self.__db_dataset["persons"]
        table.insert(dict(
            first=kwargs["first"],
            last=kwargs["last"],
            email=kwargs["email"],
            salt=kwargs["salt"],
            password=kwargs["password"],
            karma=0,
            time=int(time.time()),
        )
        )
