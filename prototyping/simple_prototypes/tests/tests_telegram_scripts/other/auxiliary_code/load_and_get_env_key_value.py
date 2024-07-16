# -*- coding: utf-8 -*-

__all__: list[str] = ["load_and_get_env_key_value"]

import prototypes.external_scripts.env_handler as env_handler


# ----------------------------------------------------------------------------
def load_and_get_env_key_value(filepath: str, environment_key: str) -> str:
    """load_and_get_env_key_value возвращает полученное значение из виртуального окружения.

    Функция предназначенна для загрузки `.env` файла в текущее виртуальное окружение,
    для дальнейшей попытки получить значение по указанному ключу.

    Args:
        filepath (str): путь к файлу, хранящему токен.
        environment_key (str): название ключа в файле и виртуальном окружении.

    Raises:
        EnvironmentError: Возбуждается если загрузка ключей не удалась.

    Returns:
        str: значение ключа, полученного из виртуального окружения.
    """
    if env_handler.load_env_file(filepath=filepath):
        key_value: str = env_handler.get_key_value_from_environment(key=environment_key)
    else:
        raise EnvironmentError(
            f"Загрузка env файла в виртуальное окружение не удалась, используя путь: {filepath}"
        )

    return key_value
