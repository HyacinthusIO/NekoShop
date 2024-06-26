# -*- coding: utf-8 -*-

"""
Модуль test_bot_state_handlers представляет из себя набор модульных тестов,
для тестирования компонентов модуля bot_state_handlers.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

import unittest
import os
import asyncio
import aiogram

from prototypes.telegram_scripts.bot_state_handlers import *
from .auxiliary_modules.get_bot_token import get_bot_token

PATH_TO_TEST_DIR: str = os.path.dirname(__file__)
TEST_DATA_DIR_NAME: str = "test_data"
ENV_FILE_NAME_WITH_CORRECT_BOT_TOKEN: str = "correct_bot_token.env"


# ____________________________________________________________________________
class BaseTestCase(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.IsolatedAsyncioTestCase.setUpClass()

        cls.path_to_bot_token_env_file: str = os.path.join(
            PATH_TO_TEST_DIR, TEST_DATA_DIR_NAME, ENV_FILE_NAME_WITH_CORRECT_BOT_TOKEN
        )

        cls.__correct_bot_token: str = get_bot_token(
            filepath=cls.path_to_bot_token_env_file, token_key="TOKEN"
        )

    # -------------------------------------------------------------------------
    async def asyncSetUp(self) -> None:
        await unittest.IsolatedAsyncioTestCase.asyncSetUp(self=self)

        self.event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self.bot: aiogram.Bot = aiogram.Bot(token=self.__correct_bot_token)
        self.dispatcher: aiogram.Dispatcher = aiogram.Dispatcher()


# ____________________________________________________________________________
class TestOnStartUpPositive(BaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseTestCase.setUpClass()

    # -------------------------------------------------------------------------
    async def asyncSetUp(self) -> None:
        await BaseTestCase.asyncSetUp(self=self)

        self.dispatcher.startup.register(callback=on_start_bot)

    # -------------------------------------------------------------------------
    async def test_successfully_activated_handler(self) -> None:
        test_task = self.event_loop.create_task(
            coro=self.dispatcher.start_polling(self.bot)  # type: ignore
        )

        try:
            async with asyncio.timeout(delay=15):
                await test_task
        except asyncio.TimeoutError:
            pass

        self.assertTrue(_current_state())


# _____________________________________________________________________________
class TestOnShutDownPositive(BaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseTestCase.setUpClass()

    # -------------------------------------------------------------------------
    async def asyncSetUp(self) -> None:
        await BaseTestCase.asyncSetUp(self=self)

        self.dispatcher.shutdown.register(callback=on_stop_bot)
        _current_state.switch_state()

    # -------------------------------------------------------------------------
    async def test_successfully_activated_handler(self) -> None:
        test_task = self.event_loop.create_task(
            coro=self.dispatcher.start_polling(self.bot)  # type: ignore
        )

        try:
            async with asyncio.timeout(delay=15):
                await test_task
        except asyncio.TimeoutError:
            pass

        self.assertFalse(_current_state())
