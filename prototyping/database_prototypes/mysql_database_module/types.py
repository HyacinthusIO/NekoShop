__all__: list[str] = [
    "AsyncMySQLConnectionType",
    "AsyncMySQLConnectMethodType",
]

from typing import Callable, Union, Coroutine, Any


from mysql.connector.aio.connection import MySQLConnection
from mysql.connector.aio.abstracts import MySQLConnectionAbstract

# Аннотация для типа подключения к MySQL БД.
AsyncMySQLConnectionType = Union[MySQLConnection, MySQLConnectionAbstract]

# Аннотация для функции, используемой для подключения к MySQL БД.
AsyncMySQLConnectMethodType = Callable[
    ..., Coroutine[Any, Any, AsyncMySQLConnectionType]
]
