# -*- coding: utf-8 -*-

"""
Модуль `interface_database_api` используется для предоставления общего интерфейса,
предоставляющего методы для реализации API для конкретных типов БД.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["Interface_DataBaseAPI"]

__author__ = "HyacinthusIO"
__version__ = "0.5.0"

from abc import ABC, abstractmethod
from typing import Any


# _____________________________________________________________________________
class Interface_DataBaseAPI(ABC):
    """Interface_DataBaseAPI интерфейс для реализации API для БД.

    Этот класс предоставляет набор общих методов для реализации конкретных типов API,
    которые будут предназначены для операций над определённым типом БД.

    Args:
        ABC (_type_): Базовый/родительский класс, позволяющий абстракцию.
    """

    @abstractmethod
    async def set_connection_with_database(self, connection: Any) -> None:
        """set_connection_with_database устанавливает соединение к БД для API.

        Данный метод должен устанавливать полученное соединение к БД,
        в соответствующий атрибут API,
        который будет отвечать за хранение активного соединения.

        Args:
            connection (Any): Соединение к БД.
        """
        pass

    @abstractmethod
    async def get_connection_with_database(self) -> Any:
        """get_connection_with_database возвращает объект подключения к БД.

        Данный метод должен возвращать объект подключения,
        который будет обеспечивать API возможностью воздействия на БД.

        Returns:
            Any: Тип возвращаемого объекта подключения.
        """
        pass

    @abstractmethod
    async def check_connection_with_database(self) -> bool:
        """check_connection_with_database проверка подключения к БД.

        Данный метод должен производить определённую проверку,
        которая определит активно ли текущее соединение к БД.

        Returns:
            bool: Активно ли?
        """
        pass
