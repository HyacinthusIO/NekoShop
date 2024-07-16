# -*- coding: utf-8 -*-

"""
Модуль manual_test_bot_start_command_handler представляет из себя ручной тест,
для тестирования компонентов модуля bot_start_command_handler.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

import sys

# Настройка перед началом ручного тестирования
sys.path.append("D:/GitRepository's/Active/NekoShop/prototyping/simple_prototypes")

import asyncio
import unittest.async_case

from tests.tests_telegram_scripts.other.auxiliary_code.base_bot_test_case_class import (
    BaseBotTestCase,
)
from prototypes.telegram_scripts.bot_start_command_handler import router, test_status


# ____________________________________________________________________________
class TestStartCommand(BaseBotTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseBotTestCase.setUpClass()

    # -------------------------------------------------------------------------
    async def asyncSetUp(self) -> None:
        await BaseBotTestCase.asyncSetUp(self=self)

        self.dispatcher.include_router(router=router)

    # -------------------------------------------------------------------------
    async def test_successfully_activated_handler(self) -> None:
        """
        Для успешного прохождения теста, требуется - после запуска бота,
        лично написать в общем чате команду: `/start`, в следствии этого бот должен будет её обработать.
        """
        test_task = self.event_loop.create_task(
            coro=self.dispatcher.start_polling(self.bot)  # type: ignore
        )

        try:
            async with asyncio.timeout(delay=15):
                await test_task

        except asyncio.TimeoutError:
            pass

        self.assertCountEqual(["OK"], test_status)


if __name__ == "__main__":
    import unittest

    unittest.main()
