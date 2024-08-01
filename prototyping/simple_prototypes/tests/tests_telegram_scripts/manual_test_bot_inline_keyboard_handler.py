# -*- coding: utf-8 -*-

"""
Модуль manual_test_bot_inline_keyboard_handler представляет из себя ручной тест,
для тестирования компонентов модуля bot_inline_keyboard_handler.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__author__ = "HyacinthusIO"
__version__ = "1.0.0"


# Настройка перед началом ручного тестирования
# .............................................................................
import sys

sys.path.append("D:/GitRepository's/Active/NekoShop/prototyping/simple_prototypes")
# .............................................................................


import asyncio

from tests.tests_telegram_scripts.other.auxiliary_code.base_bot_test_case_class import (
    BaseBotTestCase,
)
from tests.tests_telegram_scripts.other.config import TestCaseConfig
from prototypes.telegram_scripts.bot_inline_keyboard_handler import (
    router,
    test_status,
    keyboard_builder,
)


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
        лично кликнуть/нажать на кнопку, прикреплённую к сообщению от бота.
        """
        test_task = self.event_loop.create_task(
            coro=self.dispatcher.start_polling(self.bot)  # type: ignore
        )

        try:
            async with asyncio.timeout(delay=15):
                await asyncio.gather(
                    test_task,
                    self.bot.send_message(
                        chat_id=TestCaseConfig.CHAT_ID,
                        text="Тестирование Inline клавиатуры.",
                        reply_markup=keyboard_builder.as_markup(),
                    ),
                )

        except asyncio.TimeoutError:
            pass

        self.assertCountEqual(["OK"], test_status)


if __name__ == "__main__":
    import unittest

    unittest.main()
