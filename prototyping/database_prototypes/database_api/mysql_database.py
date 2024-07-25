# -*- coding: utf-8 -*-

"""
Модуль `mysql_database` предоставляет класс для представления и обработки
базы данных СУБД MySQL.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["DataBaseMySQL"]

__author__ = "HyacinthusIO"
__version__ = "0.4.0"

from database_api.database_interface import DataBaseInterface

from typing import Dict
from mysql.connector.connection_cext import CMySQLConnection
from database_api.custom_types import *


# _____________________________________________________________________________
class DataBaseMySQL(DataBaseInterface):
    def __init__(
        self,
        connect_method: MySQLConnectMethod,
        connection_data: Dict[str, str]) -> None:
        super().__init__(connect_method=connect_method, 
                         connection_data=connection_data)

    # -------------------------------------------------------------------------
    def create_connection_with_database(self) -> None:
        connect_method: MySQLConnectMethod = self.get_connect_method()
        self._connection_with_database = connect_method(**self._connection_data)

    # -------------------------------------------------------------------------
    def get_connect_method(self) -> MySQLConnectMethod:
        return self._connect_method

    # -------------------------------------------------------------------------
    async def close_connection_with_database(self) -> None:
        connection: CMySQLConnection = await self.get_connection_with_database()
        connection.close()

    # -------------------------------------------------------------------------
    async def get_connection_with_database(self) -> CMySQLConnection:
        if self._connection_with_database is None:
            self.create_connection_with_database()

        return self._connection_with_database
