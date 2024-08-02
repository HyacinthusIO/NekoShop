# -*- coding: utf-8 -*-

__all__: list[str] = ["TestCaseConfig"]

import os

from .auxiliary_code.load_and_get_env_key_value import (
    load_and_get_env_key_value,
)

from dataclasses import dataclass


# Переменные связаные с конфигурацией
PATH_TO_TEST_DATA_DIR: str = os.path.dirname(p=__file__)
TEST_DATA_DIR_NAME: str = "test_data"
ENV_FILE_NAME_WITH_API_TOKEN_BOT: str = "bot_token.env"
ENV_FILE_NAME_WITH_TELEGRAM_CHAT_ID: str = "telegram_chat_id.env"

# Полные пути к файлам конфигурации
FULL_PATH_TO_ENV_FILE_WITH_API_TOKEN_BOT: str = os.path.join(
    PATH_TO_TEST_DATA_DIR,
    TEST_DATA_DIR_NAME,
    ENV_FILE_NAME_WITH_API_TOKEN_BOT,
)

FULL_PATH_TO_ENV_FILE_WITH_TELEGRAM_CHAT_ID: str = os.path.join(
    PATH_TO_TEST_DATA_DIR,
    TEST_DATA_DIR_NAME,
    ENV_FILE_NAME_WITH_TELEGRAM_CHAT_ID,
)


# ____________________________________________________________________________
@dataclass
class TestCaseConfig:
    API_TOKEN_BOT: str = load_and_get_env_key_value(
        filepath=FULL_PATH_TO_ENV_FILE_WITH_API_TOKEN_BOT,
        environment_key="API_TOKEN_BOT",
    )

    CHAT_ID: str = load_and_get_env_key_value(
        filepath=FULL_PATH_TO_ENV_FILE_WITH_TELEGRAM_CHAT_ID,
        environment_key="CHAT_ID",
    )
