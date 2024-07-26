# -*- coding: utf-8 -*-

"""
Модуль `mysql_database_api` предоставляет класс представляющий API,
для воздействия над базой данных СУБД MySQL.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["MySQLAPI"]

__author__ = "HyacinthusIO"
__version__ = "0.4.0"

from .interface_database_api import Interface_DataBaseAPI

from mysql.connector.connection_cext import CMySQLConnection
from .custom_types import *


class MySQLAPI(Interface_DataBaseAPI):
    __connection_with_data_base: CMySQLConnection

    async def set_connection_with_database(
        self, connection: CMySQLConnection
    ) -> None:
        self.__connection_with_data_base = connection

    async def get_connection_with_database(self) -> CMySQLConnection:
        return self.__connection_with_data_base

    async def check_connection_with_database(self) -> bool:
        connection: CMySQLConnection = (
            await self.get_connection_with_database()
        )

        connection_status: bool = connection.is_connected()

        return connection_status
