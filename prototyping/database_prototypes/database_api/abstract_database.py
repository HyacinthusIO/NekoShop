# -*- coding: utf-8 -*-

"""
Модуль `abstract_database` используется для предоставления абстрактного класса,
представляющего собой базу данных.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["AbstractDataBase"]

__author__ = "HyacinthusIO"
__version__ = "0.7.1"

from abc import ABC, abstractmethod

from .interface_database_api import Interface_DataBaseAPI
from typing import Any, Callable, Dict


# _____________________________________________________________________________
class AbstractDataBase(ABC):
    """AbstractDataBase класс представляющий собой БД.

    Этот класс предоставляет основу для реализации конкретных классов,
    которые будут поддерживать подключение к различным типам баз данных.
    Он определяет методы и атрибуты, которые будут настроенны при наследовании
    в производных/дочерних классах под определённый тип БД.

    Args:
        ABC (_type_): Базовый/родительский класс, позволяющий абстракцию.

    Attributes:
        _connection_data (Dict[str, Any]): Данные для создания подключения к БД.
        _connect_method (Callable[..., Any]): Функция, используемая для установки соединения к БД.
        _connection_with_database (Any): Объект, представляющий текущее соединение к БД.
        api (Interface_DataBaseAPI): Объект, реализующий API интерфейс для определённого типа БД.
    """

    _connection_data: Dict[str, Any]
    _connect_method: Callable[..., Any]
    _connection_with_database: Any
    api: Interface_DataBaseAPI

    # -------------------------------------------------------------------------
    def __init__(
        self,
        connect_method: Callable[..., Any],
        connection_data: Dict[str, str],
        api: Interface_DataBaseAPI,
    ) -> None:
        """__init__ конструктор класса.

        При инициализации экземпляра класса,
        желательно создаввать соединение к БД.

        Args:
            connect_method (Callable[..., Any]): Функция, используемая для подключения к БД.
            connection_data (Dict[str, str]): Данные (ключевые аргументы), для аутентификации при подключении.
            api (Interface_DataBaseAPI): Объект, реализующий API интерфейс для определённого типа БД.
        """
        self._connect_method = connect_method
        self._connection_data = connection_data
        self.api = api

        self.create_connection_with_database()

    # -------------------------------------------------------------------------
    @abstractmethod
    def get_connect_method(self) -> Any:
        """get_connection_method возвращает функцию для подключения.

        Данный метод должен возвращать функцию,
        которая будет использована для установки соединения к БД.

        Returns:
            Any: Тип возвращаемого объекта функцией.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    def create_connection_with_database(self) -> None:
        """create_connection_with_database установка соединения к БД.

        Данный метод должен устанавливать соединение к БД.
        Используя метод и данные для подключения.
        *Установленное соединение следует присвоить соответствующему полю/свойству.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    def get_connection_with_database(self) -> Any:
        """get_connection_with_database возвращает объект подключения к БД.

        Данный метод должен возвращать объект подключения,
        который будет обеспечивать взаимосвязь класса и БД.

        Returns:
            Any: Тип возвращаемого объекта подключения.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    def close_connection_with_database(self) -> None:
        """close_connection_with_database закрывает подключение к БД.

        Данный метод должен закрывать текущее подключение к БД.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def connect_api_to_database(self) -> None:
        """connect_api_to_database устанавливает соединение API к БД.

        Данный метод, должен настроить соединение закреплённого API.
        Путём передачи активного соединения и вызова соответствующего метода API.
        """
        pass
