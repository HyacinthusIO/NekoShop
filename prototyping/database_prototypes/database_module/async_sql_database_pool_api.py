# -*- coding: utf-8 -*-

"""
Модуль `async_sql_database_pool_api` предоставляет общий интерфейс,
который определяет методы для реализации API для конкретных типов БД,
используя пул соединений.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["AsyncSQLDataBasePoolAPI"]

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

from abc import ABC, abstractmethod

from typing import Dict
from string import Template


# _____________________________________________________________________________
class AsyncSQLDataBasePoolAPI[PoolType, PooledConnectionType](ABC):
    """AsyncSQLDataBasePoolAPI интерфейс для реализации API для работы над БД.

    Этот абстрактный класс предоставляет интерфейс,
    содержащий набор общих методов требующих реализацию для конкретных API,
    предназначенных для выполнения операций над определёнными типами БД,
    используя пул соединений.

    *Интерфейс предполагает работу используя пул соединений для подключения к БД.

    Args:
        ABC: Базовый класс для создания абстрактных классов,
             позволяющий реализовать абстракцию.
    """

    @abstractmethod
    async def set_connection_to_pool(self, pool: PoolType) -> None:
        """set_connection_to_pool устанавливает соединение к пулу для API.

        Этот метод должен устанавливать полученный пул соединений,
        в соответствующий атрибут API, который отвечает за хранение пула.

        Args:
            pool (PoolType): Объект пула соединений.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def get_connection_from_pool(self) -> PooledConnectionType:
        """get_connection_from_pool возвращает подключения к БД из пула.

        Этот метод должен возвращать соединение из пула,
        закреплённого за API.

        Returns:
            PooledConnectionType: Объект соединения к БД из пула.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def close_connection_from_pool(
        self, connection: PooledConnectionType
    ) -> None:
        """close_connection_from_pool закрывает соединение из пула.

        Этот метод должен закрывать указанное соединение к БД,
        освобождая связанные ресурсы, возвращая соединение обратно в пул.

        Returns:
            connection (PooledConnectionType): Объект подключения, который необходимо закрыть.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def execute_sql_query_use_pool(
        self,
        query_template: Template,
        query_data: Dict[str, str],
    ) -> None:
        """execute_sql_query_use_pool выполняет запрос к БД.

        Этот метод должен выполнять запрос к БД, используя соединение из пула.
        Так же получая запрос в виде шаблона строки и данные для подстановки в запрос.

        Args:
            query_template (Template): Шаблон запроса.
            query_data (Dict[str, str]): Данные для подстановки в запрос.
        """
        pass
