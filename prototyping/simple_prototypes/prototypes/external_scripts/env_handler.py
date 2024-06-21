# -*- coding: utf-8 -*-

"""
Модуль env_handler используется для обработки файлов настройки окружения (.env),
обеспечивая загрузку пар - [ключ : значение] в виртуальное окружение и предоставляя
дополнительный функционал для взаимодействия над загруженными парами.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    "load_env_file",
    "get_key_value_from_environment",
    "normalize_env_value_type",
]

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

import os
import dotenv

from typing import Union


# ----------------------------------------------------------------------------
def load_env_file(filepath: str) -> bool:
    """load_env_file загружает '.env' файл в окружение.

    Функция загружает пары - [ключ : значение] из файла имеющего расширение '.env',
    в текущее виртуальное окружение системы.

    Args:
        filepath (str): путь к '.env' файлу.

    Raises:
        FileNotFoundError: Возбуждается если файл не существует.

    Returns:
        bool: Были ли загружены ключи в виртуальное окружение?
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не обнаружен по указанному пути: {filepath}")

    return dotenv.load_dotenv(dotenv_path=filepath)


# ----------------------------------------------------------------------------
def get_key_value_from_environment(key: str) -> str:
    """get_key_value_from_environment возвращает значение ключа из окружения.

    Функция обращается к текущему виртуальному окружению,
    для получения значения по запрашиваемому ключу.

    Args:
        key (str): запрашиваемый ключ из окружения.

    Raises:
        ValueError: Возбуждается если ключ не принадлежит окружению.

    Returns:
        str: полученное значению, по запрошенному ключу.
    """
    value: Union[str, None] = os.environ.get(key)

    if value is None:
        raise KeyError(f"Ключ {key} не существует в текущем окружении!")

    return value


# ----------------------------------------------------------------------------
def normalize_env_value_type(env_value: str) -> Union[str, int, bool]:
    """normalize_env_value_type нормализует тип данных в строке.

    Функция определяет тип данных содержащихся в строке,
    в следствии чего возвращает значение используя корректный тип данных.

    * При получении значения ключа из виртуального окружения, тип данных является строкой.

    Args:
        env_value (str): строка для нормализации.

    Returns:
        Union[str, int, bool]: Поддерживаемые типы для нормализации.
    """
    if env_value.isdigit():
        return int(env_value)
    elif env_value.lower() == "true":
        return True
    elif env_value.lower() == "false":
        return False

    return env_value
