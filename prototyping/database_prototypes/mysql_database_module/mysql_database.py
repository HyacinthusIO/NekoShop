# -*- coding: utf-8 -*-

"""
Модуль `mysql_database` реализует класс, 
который предоставляет абстракцию для работы над базами данных MySQL. 

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["MySQLDataBase"]

__author__ = "HyacinthusIO"
__version__ = "0.8.0"

from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from ..database_module.abstract_async_database import AbstractAsyncDataBase

from typing import Dict, Any
from .types import MySQLConnectionType, MySQLConnectMethodType
from .mysql_database_api import MySQLAPI


# _____________________________________________________________________________
class MySQLDataBase(
    AbstractAsyncDataBase[
        MySQLAPI, MySQLConnectMethodType, MySQLConnectionType
    ]
):
    """MySQLDataBase класс для представления MySQL БД.

    Этот класс предназначен для представления базы данных MySQL.
    Он предоставляет методы для управления соединениями БД и интеграции API,
    который будет использоваться для выполнения операций над БД.

    *Данная реализация родительского класса,
    интерпретируется использованием пула соединений, вместо одиночного соединения.

    Args:
        AbstractAsyncDataBase: Базовый класс для реализации конкретного типа БД.
    """

    __pool: MySQLConnectionPool

    # -------------------------------------------------------------------------
    def __init__(
        self,
        connect_method: MySQLConnectMethodType,
        connection_data: Dict[str, Any],
        api: MySQLAPI,
        pool_name: str = "mysql_pool",
        pool_size: int = 3,
    ) -> None:
        """__init__ конструктор.

        Инициализирует экземпляр класса MySQLDataBase.

        Args:
            connect_method (MySQLConnectMethodType): Метод подключения к базе данных.
            connection_data (Dict[str, str]): Данные для подключения к базе данных.
            api (MySQLAPI): Объект API для выполнения операций над БД.
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
    async def get_connect_method(self) -> MySQLConnectMethodType:
        """get_connect_method возвращает функцию для подключения к БД.

        Этот метод возвращает функцию,
        которая будет использована для установки соединения к БД.

        Returns:
            MySQLConnectMethod: Метод, используемый для подключения к базе данных.
        """
        return self._connect_method

    # -------------------------------------------------------------------------
    async def create_connection_with_database(self) -> None:
        """create_connection_with_database устанавливает соединение к БД.

        Этот метод создает отдельное/независимое от пула соединение,
        используя закреплённые метод и данные.

        *Установленное соединение сохраняется в атрибуте `_connection_with_database`.
        """
        connect_method: MySQLConnectMethodType = (
            await self.get_connect_method()
        )

        connection: MySQLConnectionType = connect_method(
            **self._connection_data
        )

        self._connection_with_database = connection

    # -------------------------------------------------------------------------
    async def get_connection_with_database(self) -> MySQLConnectionType:
        """get_connection_with_database возвращает объект независимого подключения к БД.

        Этот метод возвращает объект текущего,
        независимого от пула соединений, подключения к БД.

        Returns:
            MySQLConnectionType: Объект подключения к БД.
        """
        if self._connection_with_database is None:
            await self.create_connection_with_database()

        return self._connection_with_database

    # -------------------------------------------------------------------------
    async def close_connection_with_database(self) -> None:
        """close_connection_with_database закрывает текущее независимое подключение к БД.

        Этот метод закрывает текущее независимое от пула соединений, подключение к БД.
        """
        connection: MySQLConnectionType = (
            await self.get_connection_with_database()
        )

        connection.close()

    # -------------------------------------------------------------------------
    async def get_connection_from_pool(self) -> PooledMySQLConnection:
        """get_connection возвращает объект подключения к БД.

        Этот метод обращается к пулу соединений, запрашивая новое соединение.

        Returns:
            MySQLConnectionType: Объект подключения к БД.
        """
        connection: PooledMySQLConnection = self.__pool.get_connection()

        return connection

    # -------------------------------------------------------------------------
    async def close_connection_from_pool(
        self, connection: PooledMySQLConnection
    ) -> None:
        """close_connection закрывает указанное подключение к БД.

        Этот метод закрывает указанное/полученное соединение к БД,
        возвращая в пул соединений, до следующего обращения.

        Args:
            connection (MySQLConnectionType): Объект соединения к БД.
        """
        connection.close()

    # -------------------------------------------------------------------------
    async def connect_api_to_database(self) -> None:
        """connect_api_to_database устанавливает соединение API к БД.

        Этот метод настраивает соединение API к БД,
        передавая пул соединений и независимое соединение,
        обеспечивая возможность взаимодействия над БД.
        """
        pool: MySQLConnectionPool = self.__pool
        connection_with_database: MySQLConnectionType = (
            await self.get_connection_with_database()
        )

        await self.api.set_connection_with_database_with_pool(
            separate_connection=connection_with_database, pool=pool
        )
