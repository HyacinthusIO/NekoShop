# -*- coding: utf-8 -*-

"""
Модуль `async_mysql_database` реализует класс,
который предоставляет абстракцию для работы над базой данных СУБД-MySQL. 

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["AsyncMySQLDataBase"]

__author__ = "HyacinthusIO"
__version__ = "0.9.0"

from ..database_module.abstract_async_database import AbstractAsyncDataBase

from typing import Dict, Any
from mysql.connector.pooling import MySQLConnectionPool

from .types import AsyncMySQLConnectionType, AsyncMySQLConnectMethodType
from .async_mysql_database_api import AsyncMySQLAPI


# _____________________________________________________________________________
class AsyncMySQLDataBase(
    AbstractAsyncDataBase[
        AsyncMySQLAPI, AsyncMySQLConnectMethodType, AsyncMySQLConnectionType
    ]
):
    """AsyncMySQLDataBase класс для представления БД СУБД-MySQL.

    Этот класс используется для представления базы данных СУБД-MySQL.
    Он предоставляет асинхронные методы для управления подключениями к БД и для интеграции API,
    который будет использоваться для выполнения операций над БД.

    *Данная реализация родительского класса,
    интерпретируется использованием пула соединений и одиночного/независимого соединения.

    Args:
        AbstractAsyncDataBase: Базовый класс для реализации конкретного типа БД.

    Attributes:
        __pool (AsyncMySQLConnectionPool): Активный пул соединений к БД.
    """

    __pool: MySQLConnectionPool

    # -------------------------------------------------------------------------
    def __init__(
        self,
        connect_method: AsyncMySQLConnectMethodType,
        connection_data: Dict[str, Any],
        api: AsyncMySQLAPI,
        pool_name: str = "mysql_pool",
        pool_size: int = 3,
    ) -> None:
        """__init__ конструктор.

        Инициализирует экземпляр класса AsyncMySQLDataBase.

        Args:
            connect_method (AsyncMySQLConnectMethodType): Функция, используемая для независимого подключения к БД.
            connection_data (Dict[str, str]): Данные для аутентификации соединений к БД.
            api (AsyncMySQLAPI): Объект API для выполнения операций над БД.
            pool_name (str, optional): Именной идентификатор пула соединений.
                                       По умолчанию "mysql_pool".
            pool_size (int, optional): Размер/количество доступных соединений пула.
                                       По умолчанию 3.
        """
        super().__init__(
            connect_method=connect_method,
            connection_data=connection_data,
            api=api,
        )

        self.__pool = MySQLConnectionPool(
            pool_name=pool_name, pool_size=pool_size, **connection_data
        )

    # -------------------------------------------------------------------------
    async def get_connect_method(self) -> AsyncMySQLConnectMethodType:
        """get_connect_method возвращает функцию для одиночного соединения к БД.

        Этот метод возвращает функцию,
        которая будет использована для подключения одиночного/независимого соединения к БД.

        Returns:
            AsyncMySQLConnectMethodType: Функция, используемая для подключения к БД.
        """
        return self._connect_method

    # -------------------------------------------------------------------------
    async def create_connection_with_database(self) -> None:
        """create_connection_with_database устанавливает независимое подключение к БД.

        Этот метод создает отдельное/независимое от пула соединение,
        используя закреплённые метод и данные.

        *Установленное подключение сохраняется в атрибуте `_connection_with_database`.
        """
        connect_method: AsyncMySQLConnectMethodType = (
            await self.get_connect_method()
        )

        connection: AsyncMySQLConnectionType = await connect_method(
            **self._connection_data
        )

        self._connection_with_database = connection

    # -------------------------------------------------------------------------
    async def get_connection_with_database(self) -> AsyncMySQLConnectionType:
        """get_connection_with_database возвращает объект независимого подключения к БД.

        Этот метод возвращает объект текущего,
        независимого от пула соединений, подключения к БД.

        Returns:
            AsyncMySQLConnectionType: Объект подключения к БД.
        """
        if self._connection_with_database is None:
            await self.create_connection_with_database()

        return self._connection_with_database  # type: ignore

    # -------------------------------------------------------------------------
    async def close_connection_with_database(self) -> None:
        """close_connection_with_database закрывает текущее независимое соединение к БД.

        Этот метод закрывает текущее независимое от пула соединений,
        соединение к БД, тем самым обрывая независимое подключение к БД.
        """
        connection: AsyncMySQLConnectionType = (
            await self.get_connection_with_database()
        )

        await connection.close()

    # -------------------------------------------------------------------------
    async def connect_api_to_database(self) -> None:
        """connect_api_to_database устанавливает подключение API к БД.

        Этот метод настраивает соединение API к БД,
        передавая пул соединений и независимое соединение,
        обеспечивая возможность API взаимодействовать над БД.
        """
        pool: MySQLConnectionPool = self.__pool
        connection_with_database: AsyncMySQLConnectionType = (
            await self.get_connection_with_database()
        )

        await self.api.set_up(
            separate_connection=connection_with_database, pool=pool
        )
