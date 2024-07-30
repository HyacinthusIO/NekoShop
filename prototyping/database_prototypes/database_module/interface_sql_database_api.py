# -*- coding: utf-8 -*-

"""
Модуль `interface_sql_database_api` предоставляет общий интерфейс,
который определяет методы для реализации API для конкретных типов БД.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["InterfaceSQLDataBaseAPI"]

__author__ = "HyacinthusIO"
__version__ = "0.6.0"

from abc import ABC, abstractmethod
from typing import Any


# _____________________________________________________________________________
class InterfaceSQLDataBaseAPI[ConnectionType](ABC):
    """Interface_DataBaseAPI интерфейс для реализации API для работы над БД.

    Этот класс предоставляет набор общих методов для реализации конкретных типов API,
    предназначенных для операций над определёнными типами БД.

    *Интерфейс предпологает работу над одним активным подключением к БД.

    Args:
        ABC: Базовый класс для создания абстрактных классов,
             позволяющий реализовать абстракцию.
    """

    @abstractmethod
    async def set_connection_with_database(
        self, connection: ConnectionType
    ) -> None:
        """set_connection_with_database устанавливает соединение к БД для API.

        Этот метод должен устанавливать полученное соединение к БД
        в соответствующий атрибут API, который отвечает за хранение
        активного соединения.

        Args:
            connection (ConnectionType): Объект соединения к БД.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def get_connection_with_database(self) -> ConnectionType:
        """get_connection_with_database возвращает объект подключения к БД.

        Этот метод должен возвращать объект подключения,
        который позволит API взаимодействовать над БД.

        Returns:
            ConnectionType: Объект подключения к БД.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def check_connection_with_database(self) -> bool:
        """check_connection_with_database проверяет активность подключения к БД.

        Этот метод должен производить проверку, которая определит,
        активно ли текущее соединение к БД.

        Returns:
            bool: True, если соединение активно; иначе False.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def execute_sql_query_to_database(
        self, query_string: str, query_data: Any = None
    ) -> bool:
        """execute_query_to_database выполняет запрос к БД.

        Этот метод должен выполнять запрос к подключённой БД.
        Получая запрос в виде строки и данные для подстановки в запрос.

        Args:
            query_string (str): Строка запроса.
            query_data (Any, optional): Данные для подстановки в запрос.
                                        По умолчанию None.

        Returns:
            bool: True, если запрос выполнен успешно; иначе False.
        """
        pass
