"""
This module aim to manage connection pool with all kinds of connection object (connection from DB-API v2.0, ldap,...).

Start pool with one connection and grow on demand until maxconnections is reached.

The Class you deal with are Pool and ConnectionInfos.

First you have to load and build the pool : ::

    connection_infos = ConnectionInfos(connectModule, connection_name, host=host, port=port, databaseName=dbname, user=user, password=pwd)
    # Or for LDAP
    connection_infos = ConnectionInfos(connectModule, connection_name, host=host, port=port, basedn=dn, user=user, password=pwd)
    Pool.add(connection_infos)
    Pool.build(maxconnections)

.. warning::

   * ``connectModule`` must implement ``connect(cls, *args, **kwargs)`` class method which return a connection object.

Then use it : ::

    conn = Pool.get(connection_name)

    try:
        # use conn
        ...
    # Exception depend on your type of connection
    except <ConnectionLostWithServer> as e:
            # Remove all open connection if connection lost with server
            Pool.getPurge(connection_name)
    conn.close()  # Put back in pool

.. todo::

   * Detect and reset "bad" connections.
   * Currently, when connection with server is lost and came back, first request will fail (the faileur will reset all connection).
     Find a way to reset connection without a failure.
   * Set a max lifetime for connection and reset then when it's reach

"""

from Queue import Queue


class Pool():
    _infos = list()
    _pools = dict()

    @classmethod
    def add(cls, connection_infos):
        """
        Add connection's informations to the list of pools to build.

        :param ConnectionInfos connection_infos: Connection's information that will be use by the pool.
        """
        cls._infos.append(connection_infos)

    @classmethod
    def build(cls, maxconnections):
        """
        Create all connection's pools using informations in ``Pool._infos``.

        :param int maxconnections: Maximum connection for this pool.
        """
        for infos in cls._infos:
            if infos.name not in cls._pools:
                cls._pools[infos.name] = ConnectionPool(infos.connectModule, maxconnections, **infos.opts)

    @classmethod
    def getConnection(cls, connection_name):
        return cls._pools[connection_name].getConnection()

    @classmethod
    def getPurge(cls, connection_name):
        cls._pools[connection_name].purgeQueu()


class ConnectionInfos(object):
    """ Store connection informations.

    :param connectModule: Instance of python module used to establish connection.
    :param str name: The name of this connection informations, **MUST** be unique.
    :param kwargs: Other arguments which are driver specific.
    """
    def __init__(self, connectModule, name, **kwargs):
        self.connectModule = connectModule
        self.name = name
        self.opts = kwargs
        for name, value in kwargs.items():
            setattr(self, name, value)


class ConnectionWrapper:
    """
    Create a proxy for pooled connections.

    :param pool: The connection pool itself.
    :param con: A established connection.
    """

    def __init__(self, pool, con):
        self._con = con
        self._pool = pool

    def close(self):
        """
        Return the connection to the pool.
        """
        if self._con is not None:
            self._pool.putConnection(self._con)
            self._con = None

    def __getattr__(self, name):
        return getattr(self._con, name)

    def __del__(self):
        self.close()


class ConnectionPool:
    """ Create a new connection pool.

    :param connectModule: Instance of module use to establish a connection.

        .. important::

            ``connectModule.connect(*args, **kwargs)`` must return a connection Instance.

    :param str int: Maximum number of connection in the pool.
    """
    def __init__(self, connectModule, maxconnections, *args, **kwargs):
        self.connectModule = connectModule
        self.args = args
        self.kwargs = kwargs

        self._queue = Queue(maxconnections)

        self.putConnection(self.connectModule.connect(*self.args, **self.kwargs))

    def getConnection(self):
        """Get a connection from the pool or create new one if queu is empty."""
        if self._queue.empty():
            return ConnectionWrapper(self, self.connectModule.connect(*self.args, **self.kwargs))
        else:
            return ConnectionWrapper(self, self._queue.get())

    def putConnection(self, con):
        """Put a connection to the pool if the pool is not full."""
        if not self._queue.full():
            self._queue.put(con)

    def purgeQueu(self):
        """ Clear the queu. """
        with self._queue.mutex:
            self._queue.queue.clear()
