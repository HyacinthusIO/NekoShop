# -*- coding: utf-8 -*-

"""
Модуль `abstract_async_database` предоставляет базовый абстрактный класс,
который будет представлять базу данных.

Конкретные реализации базы данных будут наследоваться от этого абстрактного класса
и реализовывать методы для работы над определенной БД (СУБД).

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["AbstractAsyncDataBase"]

__author__ = "HyacinthusIO"
__version__ = "0.9.2"

from abc import ABC, abstractmethod

from typing import Any, Dict, Optional


# _____________________________________________________________________________
class AbstractAsyncDataBase[APIType, ConnectMethodType, ConnectionType](ABC):
    """AbstractAsyncDataBase класс для представления базы данных.

    Этот класс служит основой для реализации конкретных классов,
    поддерживающих подключение к определённому типу базы данных.
    Он определяет методы и атрибуты, которые должны быть
    реализованы в производных классах для работы над конкретными типами БД (СУБД).

    *Класс не должен поддерживать прямое взаимодействие над БД,
    для этого должен быть реализован и подключён API.

    Args:
        ABC: Базовый класс для создания абстрактных классов,
             позволяющий реализовать абстракцию.

    Attributes:
        _connection_data (Dict[str, Any]): Данные, необходимые для установки соединения к БД.
        _connect_method (ConnectMethodType): Функция, используемая для установки соединения к БД.
        _connection_with_database (Optional[ConnectionType]): Объект, представляющий текущее подключение к БД.
                                                              По умолчанию None.
        api (APIType): Объект, реализующий API для работы над конкретным типом БД.
    """

    _connection_data: Dict[str, Any]
    _connect_method: ConnectMethodType
    _connection_with_database: Optional[ConnectionType] = None
    api: APIType

    # -------------------------------------------------------------------------
    def __init__(
        self,
        connect_method: ConnectMethodType,
        connection_data: Dict[str, Any],
        api: APIType,
    ) -> None:
        """__init__ конструктор.

        Args:
            connect_method (ConnectMethodType): Функция, используемая для подключения к БД.
            connection_data (Dict[str, str]): Данные (ключевые аргументы), для аутентификации.
            api (APIType): Объект, реализующий API для определённого типа БД.
        """
        self._connect_method = connect_method
        self._connection_data = connection_data
        self.api = api

    # -------------------------------------------------------------------------
    @abstractmethod
    async def get_connect_method(self) -> ConnectMethodType:
        """get_connect_method возвращает функцию для подключения к БД.

        Этот метод должен возвращать функцию,
        которая будет использована для установки соединения к БД.

        Returns:
            ConnectMethodType: Функция для подключения к БД.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def create_connection_with_database(self) -> None:
        """create_connection_with_database устанавливает соединение к БД.

        Этот метод должен устанавливать соединение к БД,
        используя метод и данные для создания подключения.

        *Установленное подключение следует присвоить соответствующему атрибуту.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def get_connection_with_database(self) -> ConnectionType:
        """get_connection_with_database возвращает объект подключения к БД.

        Этот метод должен возвращать объект подключения,
        который обеспечит взаимодействие класса над БД.

        *Если подключение не было установленно до вызова данного метода,
        следует вызвать метод для создания подключения.

        Returns:
            ConnectionType: Объект подключения к БД.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def close_connection_with_database(self) -> None:
        """close_connection_with_database закрывает текущее соединение к БД.

        Этот метод должен закрывать текущее подключение к БД,
        которое присвоено соответствующему атрибуту.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def connect_api_to_database(self) -> None:
        """connect_api_to_database устанавливает подключение API к БД.

        Этот метод должен настраивать соединение установленного API к БД,
        вызывая соответствующий метод API для настройки.
        """
        pass
