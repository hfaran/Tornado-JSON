import torndb
import dataset


class MySQLConnection(object):

    """Base class for connecting to a MySQL DB

    - torndb should be used for custom SQL queries
    - dataset is encouraged for simple find and insert queries

    Create torndb and dataset connections to database

    :type  host: str
    :param host: <IPAddr>:<port> of MySQL server
    :type  database: str
    :param database: Name of database to connect to
    :type  user: str
    :param user: MySQL username
    :type  password: str
    :param password: MySQL password
    """

    def __init__(self, host, database, user, password):
        self._db_torndb = torndb.Connection(
            host=host,
            database=database,
            user=user,
            password=password,
        )
        self._db_dataset = dataset.connect(
            "mysql://{}:{}@{}/{}".format(
                user,
                password,
                host,
                database,
            )
        )

    def generic_query(self, method, query, parameters=None, force=False):
        """torndb.Connection.method(query, *parameters)

        This method attempts to force proper parameterization of SQL
        queries to prevent SQL injection.

        - Any direct queries to the database MUST be made with this method
        - This method does not yet support kwparameters (if needed, will add)

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
