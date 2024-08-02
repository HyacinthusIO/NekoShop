# -*- coding: utf-8 -*-

__all__: list[str] = ["BaseBotTestCase"]

import unittest
import asyncio
import aiogram

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

        cls._correct_bot_token: str = Config.API_TOKEN_BOT

    # -------------------------------------------------------------------------
    async def asyncSetUp(self) -> None:
        await unittest.IsolatedAsyncioTestCase.asyncSetUp(self=self)

        self.event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self.bot: aiogram.Bot = aiogram.Bot(token=self._correct_bot_token)
        self.dispatcher: aiogram.Dispatcher = aiogram.Dispatcher()
