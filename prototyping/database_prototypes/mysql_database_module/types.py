__all__: list[str] = ["MySQLConnectionType", "MySQLConnectMethodType"]

from typing import Callable, Union

from mysql.connector.aio.connection import MySQLConnection
from mysql.connector.connection_cext import CMySQLConnection

# Аннотация для типа подключения к MySQL БД.
MySQLConnectionType = Union[MySQLConnection, CMySQLConnection]

# Аннотация для функции, используемой для подключения к MySQL БД.
MySQLConnectMethodType = Callable[..., MySQLConnectionType]
