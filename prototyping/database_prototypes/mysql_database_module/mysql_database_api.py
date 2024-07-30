# -*- coding: utf-8 -*-

"""
Модуль `mysql_database_api` предоставляет класс представляющий API,
для взаимодействия над дазой данных, СУБД MySQL.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["MySQLAPI"]

__author__ = "HyacinthusIO"
__version__ = "0.6.1"

from typing import Any

from ..database_module.interface_sql_database_api import (
    InterfaceSQLDataBaseAPI,
)
from .types import MySQLConnectionType

from typing import Optional
from mysql.connector.pooling import PooledMySQLConnection, MySQLConnectionPool


class MySQLAPI(InterfaceSQLDataBaseAPI[MySQLConnectionType]):
    __pool: Optional[MySQLConnectionPool]
    __connection_with_database: MySQLConnectionType

    # ------------------------------------------------------------------------
    async def set_connection_with_database_with_pool(
        self,
        separate_connection: MySQLConnectionType,
        pool: Optional[MySQLConnectionPool] = None,
    ) -> None:
        self.__pool = pool
        await self.set_connection_with_database(connection=separate_connection)

    # ------------------------------------------------------------------------
    async def set_connection_with_database(
        self, connection: MySQLConnectionType
    ) -> None:
        self.__connection_with_database

    # ------------------------------------------------------------------------
    async def get_connection_with_database(self) -> MySQLConnectionType:
        return self.__connection_with_database

    # ------------------------------------------------------------------------
    async def check_connection_with_database(self) -> bool:
        connection: MySQLConnectionType = (
            await self.get_connection_with_database()
        )

        connection_status: bool = connection.is_connected()

        return connection_status

    async def execute_sql_query_to_database(
        self, query_string: str, query_data: Any = None
    ) -> bool:
        pass
