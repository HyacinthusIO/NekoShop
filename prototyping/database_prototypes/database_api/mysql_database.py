# -*- coding: utf-8 -*-

"""
Модуль `mysql_database` предоставляет класс для представления и обработки
базы данных СУБД MySQL.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["MySQLDataBase"]

__author__ = "HyacinthusIO"
__version__ = "0.5.1"

from .abstract_database import AbstractDataBase

from typing import Dict
from mysql.connector.connection_cext import CMySQLConnection
from .custom_types import *
from .mysql_database_api import MySQLAPI


# _____________________________________________________________________________
class MySQLDataBase(AbstractDataBase):
    def __init__(
        self,
        connect_method: MySQLConnectMethod,
        connection_data: Dict[str, str],
        api: MySQLAPI,
    ) -> None:
        super().__init__(
            connect_method=connect_method,
            connection_data=connection_data,
            api=api,
        )

    # -------------------------------------------------------------------------
    def get_connect_method(self) -> MySQLConnectMethod:
        return self._connect_method

    # -------------------------------------------------------------------------
    def create_connection_with_database(self) -> None:
        connect_method: MySQLConnectMethod = self.get_connect_method()
        connection: MySQLConnection = connect_method(**self._connection_data)

        self._connection_with_database = connection

    # -------------------------------------------------------------------------
    def get_connection_with_database(self) -> CMySQLConnection:
        if self._connection_with_database is None:
            self.create_connection_with_database()

        return self._connection_with_database

    # -------------------------------------------------------------------------
    def close_connection_with_database(self) -> None:
        connection: CMySQLConnection = self.get_connection_with_database()

        connection.close()

    # -------------------------------------------------------------------------
    async def connect_api_to_database(self) -> None:
        connection: CMySQLConnection = self.get_connection_with_database()

        await self.api.set_connection_with_database(connection=connection)
