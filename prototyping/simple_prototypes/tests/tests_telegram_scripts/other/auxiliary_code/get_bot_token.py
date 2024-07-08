# -*- coding: utf-8 -*-

__all__: list[str] = ["get_bot_token"]

import prototypes.external_scripts.env_handler as env_handler


# ----------------------------------------------------------------------------
def get_bot_token(filepath: str, token_key: str) -> str:
    """get_bot_token возвращает полученный токен из виртуального окружения.

    Функция предназначенна для загрузки `.env` файла в текущее виртуальное окружение,
    в целях получить токен для telegram бота.

    Args:
        filepath (str): путь к файлу, хранящему токен.
        token_key (str): название ключа в файле и виртуальном окружении.

    Raises:
        EnvironmentError: Возбуждается если загрузка ключей не удалась.

    Returns:
        str: токен telegram бота полученный из виртуального окружения.
    """
    if env_handler.load_env_file(filepath=filepath):
        correct_bot_token: str = env_handler.get_key_value_from_environment(
            key=token_key
        )
    else:
        raise EnvironmentError(
            f"Загрузка токена бота в виртуальное окружение не удалась, используя путь: {filepath}"
        )

    return correct_bot_token
