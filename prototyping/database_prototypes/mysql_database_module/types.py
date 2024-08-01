# -*- coding: utf-8 -*-

"""
Модуль предназначен для хранения кастомных типов,
для обеспечения корректной аннотации в используемом коде.
"""

__all__: list[str] = [
    "AsyncMySQLConnectionType",
    "AsyncMySQLConnectMethodType",
    "MySQLPooledConnection",
]

from typing import Callable, Union, Coroutine, Any

from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.connection_cext import CMySQLConnection
from mysql.connector.aio.connection import MySQLConnection
from mysql.connector.aio.abstracts import MySQLConnectionAbstract


# Аннотация для типа независимого асинхронного соединения к MySQL.
AsyncMySQLConnectionType = Union[MySQLConnection, MySQLConnectionAbstract]

# Аннотация для функции, используемой для установки асинхронного соединения к MySQL.
AsyncMySQLConnectMethodType = Callable[
    ..., Coroutine[Any, Any, AsyncMySQLConnectionType]
]

# Аннотация для типа соединения из пула к MySQL.
MySQLPooledConnection = Union[PooledMySQLConnection, CMySQLConnection]
