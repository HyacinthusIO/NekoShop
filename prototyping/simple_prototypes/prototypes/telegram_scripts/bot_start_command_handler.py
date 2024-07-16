# -*- coding: utf-8 -*-

"""
Модуль bot_start_command_handler используяется для демонстрации работы
обработчика команд бота.
(Прямое использование данного модуля в разработке конечного продукта не предусмотренно)

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["router", "test_status"]

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

from aiogram import Router

from aiogram.types import Message
from aiogram.filters import Command


router = Router(name=__name__)
test_status: list[str] = []


# -----------------------------------------------------------------------------
@router.message(Command("start", ignore_case=True))
async def cmd_start(msg: Message) -> None:
    test_status.append("OK")
