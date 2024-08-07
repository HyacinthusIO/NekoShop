# -*- coding: utf-8 -*-

"""
Модуль `async_sql_database_api` предоставляет общий интерфейс,
который определяет методы для реализации API для конкретных типов БД,
используя одиночное асинхронное соединение.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["AsyncSQLDataBaseAPI"]

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

from abc import ABC, abstractmethod

from typing import Dict
from string import Template


# _____________________________________________________________________________
class AsyncSQLDataBaseAPI[ConnectionType](ABC):
    """AsyncSQLDataBaseAPI интерфейс для реализации API для работы над БД.

    Этот класс предоставляет интерфейс,
    содержащий набор асинхронных методов для реализации конкретных типов API,
    предназначенных для выполнения операций над определёнными типами БД.

    *Интерфейс предпологает работу над одним соединением обеспечивающим подключение к БД.
    Данное соединение, должно поддерживать асинхронность.

    Args:
        ABC: Базовый класс для создания абстрактных классов,
             позволяющий реализовать абстракцию.
    """

    @abstractmethod
    async def set_connection_with_database(
        self, connection: ConnectionType
    ) -> None:
        """set_connection_with_database устанавливает соединение к БД для API.

        Этот метод должен устанавливать полученное соединение к БД,
        в соответствующий атрибут API, который отвечает за хранение соединения.

        Args:
            connection (ConnectionType): Объект соединения к БД.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def get_connection_with_database(self) -> ConnectionType:
        """get_connection_with_database возвращает подключение к БД.

        Этот метод должен возвращать объект соединения,
        который обеспечивает подключение к БД и позволит API выполнять манипуляции над БД.

        Returns:
            ConnectionType: Объект соединения к БД.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def check_connection_with_database(self) -> bool:
        """check_connection_with_database проверяет активность подключения к БД.

        Этот метод должен производить проверку, которая определит,
        активно ли текущее подключение к БД.

        Returns:
            bool: True, если соединение активно; иначе False.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def execute_sql_query_to_database(
        self, query_template: Template, query_data: Dict[str, str]
    ) -> None:
        """execute_sql_query_to_database выполняет запрос к БД.

        Этот метод должен выполнять запрос к подключённой БД.
        Получая запрос в виде строки и данные для подстановки в запрос.

        Args:
            query_template (Template): Шаблон запроса.
            query_data (Dict[str, str]): Данные для подстановки в запрос.
        """
        pass
