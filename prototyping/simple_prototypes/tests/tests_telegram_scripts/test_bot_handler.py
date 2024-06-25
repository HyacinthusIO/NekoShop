# -*- coding: utf-8 -*-

"""
Модуль test_bot_handler представляет из себя набор модульных тестов,
для тестирования компонентов модуля bot_handler.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__author__ = "HyacinthusIO"
__version__ = "1.0.1"

import unittest
import aiogram
import asyncio
import os

import aiogram.exceptions

from prototypes.telegram_scripts.bot_handler import *
from .auxiliary_modules.get_bot_token import get_bot_token

from aiogram.client.default import DefaultBotProperties
from aiogram.utils.token import TokenValidationError


PATH_TO_TEST_DIR: str = os.path.dirname(__file__)
TEST_DATA_DIR_NAME: str = "test_data"
ENV_FILE_NAME_WITH_CORRECT_BOT_TOKEN: str = "correct_bot_token.env"


# ____________________________________________________________________________
class TestCreateDispatcherPositive(unittest.IsolatedAsyncioTestCase):
    async def test_successful_dispatcher_creation(self) -> None:
        telegram_dispatcher: aiogram.Dispatcher = await create_dispatcher()

        self.assertIsInstance(obj=telegram_dispatcher, cls=aiogram.Dispatcher)

    # ------------------------------------------------------------------------
    async def test_function_accepts_other_kwargs(self) -> None:
        dispatcher_name: str = "TestDispatcher"

        telegram_dispatcher: aiogram.Dispatcher = await create_dispatcher(
            name=dispatcher_name
        )

        self.assertEqual(first=dispatcher_name, second=telegram_dispatcher.name)


# ____________________________________________________________________________
class TestCreateDispatcherNegative(unittest.IsolatedAsyncioTestCase):
    async def test_not_default_kwargs_in_workflow_data(self) -> None:
        telegram_dispatcher: aiogram.Dispatcher = await create_dispatcher(
            strawberry="banana"
        )

        self.assertIn(
            member="strawberry", container=telegram_dispatcher.workflow_data.keys()
        )


# ____________________________________________________________________________
class TestConfigureBotPositive(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.IsolatedAsyncioTestCase.setUpClass()

        cls.path_to_bot_token_env_file: str = os.path.join(
            PATH_TO_TEST_DIR, TEST_DATA_DIR_NAME, ENV_FILE_NAME_WITH_CORRECT_BOT_TOKEN
        )

        cls.__correct_bot_token: str = get_bot_token(
            filepath=cls.path_to_bot_token_env_file, token_key="TOKEN"
        )

    # ------------------------------------------------------------------------
    async def test_successful_bot_setup(self) -> None:
        bot: aiogram.Bot = await configure_bot(bot_token=self.__correct_bot_token)

        self.assertIsInstance(obj=bot, cls=aiogram.Bot)

    # ------------------------------------------------------------------------
    async def test_default_parse_mode_is_html(self) -> None:
        bot: aiogram.Bot = await configure_bot(bot_token=self.__correct_bot_token)

        self.assertEqual(
            first=aiogram.enums.ParseMode.HTML, second=bot.default.parse_mode
        )

    # ------------------------------------------------------------------------
    async def test_function_get_DefaultBotProperties(self) -> None:
        bot: aiogram.Bot = await configure_bot(
            bot_token=self.__correct_bot_token,
            default_param=DefaultBotProperties(
                disable_notification=True, allow_sending_without_reply=True
            ),
        )

        self.assertTrue(bot.default.disable_notification)
        self.assertTrue(bot.default.allow_sending_without_reply)


# ____________________________________________________________________________
class TestConfigureBotNegative(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.IsolatedAsyncioTestCase.setUpClass()

        cls.invalid_bot_token: str = "15657273zdgfohgw"  # Формат токена не корректный

    # -------------------------------------------------------------------------
    async def test_invalid_bot_token_raise_TokenValidationError(self) -> None:
        with self.assertRaises(expected_exception=TokenValidationError):
            await configure_bot(bot_token=self.invalid_bot_token)

    # -------------------------------------------------------------------------
    @unittest.expectedFailure
    async def test_incorrect_kwargs_raise_exception(self) -> None:
        await configure_bot(bot_token="999999:hhhhhhhh", banana="strawberry")  # type: ignore


# ____________________________________________________________________________
class TestRunBotPositive(unittest.IsolatedAsyncioTestCase):
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
        await unittest.IsolatedAsyncioTestCase.asyncSetUp(self)

        self.event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self.bot: aiogram.Bot = await configure_bot(bot_token=self.__correct_bot_token)
        self.dispatcher: aiogram.Dispatcher = await create_dispatcher()

    # -------------------------------------------------------------------------
    async def test_successful_bot_launch(self) -> None:
        test_task = self.event_loop.create_task(
            run_bot(bot=self.bot, dispatcher=self.dispatcher)
        )

        try:
            async with asyncio.timeout(delay=15):
                await test_task
        except asyncio.TimeoutError:
            pass


# ____________________________________________________________________________
class TestRunBotNegative(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        unittest.IsolatedAsyncioTestCase.setUpClass()

        cls.incorrect_bot_token: str = "99999:hhhhhhh"

    # -------------------------------------------------------------------------
    async def asyncSetUp(self) -> None:
        await unittest.IsolatedAsyncioTestCase.asyncSetUp(self)

        self.event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self.bot: aiogram.Bot = await configure_bot(bot_token=self.incorrect_bot_token)
        self.dispatcher: aiogram.Dispatcher = await create_dispatcher()

    # -------------------------------------------------------------------------
    async def test_incorrect_bot_token(self) -> None:
        test_task = self.event_loop.create_task(
            run_bot(bot=self.bot, dispatcher=self.dispatcher)
        )

        with self.assertRaises(
            expected_exception=aiogram.exceptions.TelegramUnauthorizedError
        ):
            await test_task
