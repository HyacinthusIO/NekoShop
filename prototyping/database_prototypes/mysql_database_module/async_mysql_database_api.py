# -*- coding: utf-8 -*-

"""
Модуль `async_mysql_database_api` предоставляет класс представляющий API,
для взаимодействия над базой данных, СУБД-MySQL.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["AsyncMySQLAPI"]

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

from ..database_module.async_sql_database_api import (
    AsyncSQLDataBaseAPI,
)
from ..database_module.async_sql_database_pool_api import (
    AsyncSQLDataBasePoolAPI,
)

from typing import Dict
from string import Template
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector.errors import Error as MySQLError

from .types import (
    AsyncMySQLConnectionType,
    MySQLPooledConnection,
)


class AsyncMySQLAPI(
    AsyncSQLDataBaseAPI[AsyncMySQLConnectionType],
    AsyncSQLDataBasePoolAPI[MySQLConnectionPool, MySQLPooledConnection],
):
    """AsyncMySQLAPI класс для представления API для БД СУБД-MySQL.

    Этот класс предназначен для представления API.
    Он предоставляет асинхронные методы для управления соединениями пула и независимым соединением к БД.

    *Независимое соединение используется для прямого подключения к БД.
    Пул соединений используется для запросов приложения, использующего данный API.

    Args:
        AsyncSQLDataBaseAPI: Интерфейс для реализации API одиночного соединения.
        AsyncSQLDataBasePoolAPI: Интерфейс для реализации API пула соединений.

    Attributes:
        __pool (AsyncMySQLConnectionPool): Активный пул соединений к БД
        __connection_with_database (AsyncMySQLConnectionType): Активное независимое подключение к БД.
    """

    __pool: MySQLConnectionPool
    __connection_with_database: AsyncMySQLConnectionType

    async def set_up(
        self,
        separate_connection: AsyncMySQLConnectionType,
        pool: MySQLConnectionPool,
    ) -> None:
        """set_up настраивает API.

        Этот метод используется для первичной настройки API.
        Вызывая соответствующие методы для установки независимого и пула соединений.

        Args:
            separate_connection (AsyncMySQLConnectionType): Независимое соединение к БД.
            pool (MySQLConnectionPool): Пул соединений к БД.
        """
        await self.set_connection_with_database(connection=separate_connection)
        await self.set_connection_to_pool(pool=pool)

    # -------------------------------------------------------------------------
    async def set_connection_to_pool(self, pool: MySQLConnectionPool) -> None:
        """set_connection_to_pool подключает пул соединений к API.

        Этот метод устанавливает полученный пул соединений к БД,
        в соответствующий атрибут API, отвечающий за хранение пула соединений.

        Args:
            pool (MySQLConnectionPool): Пул соединений к БД.
        """
        self.__pool = pool

    # -------------------------------------------------------------------------
    async def set_connection_with_database(
        self, connection: AsyncMySQLConnectionType
    ) -> None:
        """set_connection_with_database устанавливает соединение к БД для API.

        Этот метод устанавливает соединение к БД,
        в соответствующий атрибут API, отвечающий за хранение независимого соединения.

        Args:
            connection (AsyncMySQLConnectionType): Независимое соединение к БД.
        """
        self.__connection_with_database = connection

    # -------------------------------------------------------------------------
    async def get_connection_with_database(self) -> AsyncMySQLConnectionType:
        """get_connection_with_database возвращает независимое подключение к БД.

        Этот метод возвращает объект независимого подключения,
        установленным в соответствующем атрибуте API.

        *Независимое подключение является асинхронным.

        Returns:
            AsyncMySQLConnectionType: Объект подключения к БД.
        """
        return self.__connection_with_database

    # -------------------------------------------------------------------------
    async def get_connection_from_pool(self) -> MySQLPooledConnection:
        """get_connection_from_pool возвращает объект подключения к БД из пула.

        Этот метод возвращает объект подключения из пула.

        *Соединения в пуле, являются синхронными.

        Returns:
            MySQLPooledConnection: Объект соединения к БД из пула.
        """
        connection: MySQLPooledConnection = self.__pool.get_connection()

        return connection

    # -------------------------------------------------------------------------
    async def check_connection_with_database(self) -> bool:
        """check_connection_with_database проверяет активность прямого подключения к БД.

        Этот метод производит проверку,
        определяющую активно ли текущее независимое соединение к БД.

        Returns:
            bool: True, если подключение активно; иначе False.
        """
        connection: AsyncMySQLConnectionType = (
            await self.get_connection_with_database()
        )

        connection_status: bool = await connection.is_connected()

        return connection_status

    # -------------------------------------------------------------------------
    async def close_connection_from_pool(
        self, connection: MySQLPooledConnection
    ) -> None:
        """close_connection_from_pool закрывает соединение из пула.

        Этот метод закрывает указанное соединение к БД,
        возвращая соединение обратно в пул.

        Args:
            connection (MySQLPooledConnection): Объект соединения из пула.
        """
        connection.close()

    # -------------------------------------------------------------------------
    async def execute_sql_query_use_pool(
        self,
        query_template: Template,
        query_data: Dict[str, str],
    ) -> None:
        """execute_sql_query_use_pool выполняет запрос к БД.

        Этот метод выполняет запрос к БД, используя соединение из пула.
        Для генерации запроса используется шаблон запроса и данные для подстановки в него.

        Args:
            query_template (Template): Шаблон строки запроса.
            query_data (Dict[str, str]): Данные для подстановки в шаблон.
        """
        connection: MySQLPooledConnection = (
            await self.get_connection_from_pool()
        )

        query_string: str = query_template.substitute(**query_data)

        try:
            with connection.cursor() as cursor:
                cursor.execute(query_string)

                connection.commit()

        except MySQLError as error:
            connection.rollback()
            print(f"Возникла ошибка при выполнении запроса! {error}")

        finally:
            await self.close_connection_from_pool(connection=connection)

    # -------------------------------------------------------------------------
    async def execute_sql_query_to_database(
        self, query_template: Template, query_data: Dict[str, str]
    ) -> None:
        """execute_sql_query_to_database выполняет запрос к БД.

        Этот метод выполняет запрос к БД, используя независимое соединение.
        Для генерации запроса используется шаблон запроса и данные для подстановки в него.

        Args:
            query_template (Template): Шаблон строки запроса.
            query_data (Dict[str, str]): Данные для подстановки в шаблон.
        """
        connection: AsyncMySQLConnectionType = (
            await self.get_connection_with_database()
        )

        query_string: str = query_template.substitute(**query_data)

        try:
            async with await connection.cursor() as cursor:
                await cursor.execute(query_string)

                await connection.commit()

        except MySQLError as error:
            await connection.rollback()
            print(f"Возникла ошибка при выполнении запроса! {error}")
