# -*- coding: utf-8 -*-

"""
Модуль bot_inline_keyboard_handler используяется для демонстрации работы
функциональности `inline` клавиатуры и `callback_query`.
(Прямое использование данного модуля в разработке конечного продукта не предусмотренно)


Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["router", "test_status", "keyboard_builder"]

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, CallbackQuery


router = Router(name=__name__)
test_status: list[str] = []

# Keyboard
keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
keyboard_button: InlineKeyboardButton = InlineKeyboardButton(
    text="Click me!", callback_data="Button is clicked!"
)
keyboard_builder.add(keyboard_button)


# CallbackQuery
@router.callback_query()
async def callback_click_me(query: CallbackQuery) -> None:
    if query.data == "Button is clicked!":
        test_status.append("OK")

    await query.answer(text="Callback is accepted!")
