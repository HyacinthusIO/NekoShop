__all__: list[str] = ["MySQLConnection", "MySQLConnectMethod"]


from typing import Callable, Union
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract


MySQLConnection = Union[PooledMySQLConnection, MySQLConnectionAbstract]
MySQLConnectMethod = Callable[..., MySQLConnection]
