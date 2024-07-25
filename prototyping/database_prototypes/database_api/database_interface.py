# -*- coding: utf-8 -*-

"""
Модуль `database_interface` используется для предоставления абстрактного класса,
представляющего общий интерфейс для представления базы данных.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["DataBaseInterface"]

__author__ = "HyacinthusIO"
__version__ = "0.6.0"

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict


# _____________________________________________________________________________
class DataBaseInterface(ABC):
    """DataBaseInterface интерфейс представляющий БД.

    Этот класс предоставляет основу для реализации конкретных классов,
    которые будут поддерживать подключение к различным типам баз данных.
    Он определяет методы и атрибуты, которые будут настроенны при наследовании
    в производных/дочерних классах под определённый тип БД.

    Args:
        ABC (_type_): базовый/родительский класс.

    Attributes:
        _connection_data (Dict[str, Any]): Данные для аутентификации при подключении к БД.
        _connect_method (Callable[..., Any]): Функция, используемая для установки соединения к БД.
        _connection_with_database (Any): Объект, представляющий текущее соединение к БД.
    """

    _connection_data: Dict[str, Any]
    _connect_method: Callable[..., Any]
    _connection_with_database: Any

    # -------------------------------------------------------------------------
    def __init__(
        self,
        connect_method: Callable[..., Any],
        connection_data: Dict[str, str]) -> None:
        """__init__ конструктор класса.

        При инициализации экземпляра класса,
        желательно создаввать соединение к БД.

        Args:
            connect_method (Callable[..., Any]): Функция, используемая для подключения к БД.
            connection_data (Dict[str, str]): Данные (ключевые аргументы), для аутентификации при подключении.
        """
        self._connect_method = connect_method
        self._connection_data = connection_data

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
        """create_connection установка соединения к БД.

        Данный метод должен устанавливать соединение к БД.
        Используя метод и данные для подключения.
        *Установленное соединение следует присвоить соответствующему полю/свойству.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def get_connection_with_database(self) -> Any:
        """get_connection возвращает объект подключения к БД.

        Данный метод должен возвращать объект подключения,
        который будет обеспечивать взаимосвязь класса и БД.

        Returns:
            Any: Тип возвращаемого объекта подключения.
        """
        pass

    # -------------------------------------------------------------------------
    @abstractmethod
    async def close_connection_with_database(self) -> None:
        """get_connection закрывает подключение к БД.

        Данный метод должен закрывать текущее подключение к БД.
        """
        pass
