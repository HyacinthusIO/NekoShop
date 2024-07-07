# -*- coding: utf-8 -*-

__all__: list[str] = ["BaseBotTestCase"]

import unittest
import os
import asyncio
import aiogram

from .get_bot_token import get_bot_token
from ..config import TestCaseConfig as Config


# ____________________________________________________________________________
class BaseBotTestCase(unittest.IsolatedAsyncioTestCase):
    """BaseTestCase базовый класс, для тестирования функциональности бота.

    Базовый класс избавляющий от дублирования кода в настройках тестовых случаев,
    обеспечивает простой настройкой и подготовкой к запуску бота.
    """

    @classmethod
    def setUpClass(cls) -> None:
        unittest.IsolatedAsyncioTestCase.setUpClass()

        cls.path_to_bot_token_env_file: str = os.path.join(
            Config.PATH_TO_TEST_DATA_DIR,
            Config.TEST_DATA_DIR_NAME,
            Config.ENV_FILE_NAME_WITH_CORRECT_BOT_TOKEN,
        )

        cls._correct_bot_token: str = get_bot_token(
            filepath=cls.path_to_bot_token_env_file, token_key="TOKEN"
        )

    # -------------------------------------------------------------------------
    async def asyncSetUp(self) -> None:
        await unittest.IsolatedAsyncioTestCase.asyncSetUp(self=self)

        self.event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self.bot: aiogram.Bot = aiogram.Bot(token=self._correct_bot_token)
        self.dispatcher: aiogram.Dispatcher = aiogram.Dispatcher()
