# -*- coding: utf-8 -*-

__all__: list[str] = ["TestCaseConfig"]

import os

from dataclasses import dataclass


@dataclass
class TestCaseConfig:
    PATH_TO_TEST_DATA_DIR: str = os.path.dirname(p=__file__)
    TEST_DATA_DIR_NAME: str = "test_data"
    ENV_FILE_NAME_WITH_CORRECT_BOT_TOKEN: str = "correct_bot_token.env"
