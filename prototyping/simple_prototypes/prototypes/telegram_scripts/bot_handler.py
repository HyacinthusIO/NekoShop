# -*- coding: utf-8 -*-

"""
Модуль bot_handler используется для обработки, включая настройку требуемых компонентов,
для запуска telegram бота.

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

__all__: list[str] = ["create_dispatcher", "configure_bot", "run_bot"]

__author__ = "HyacinthusIO"
__version__ = "1.0.0"

from aiogram import Dispatcher, Bot

from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from typing import Any


# ----------------------------------------------------------------------------
async def create_dispatcher(**kwargs: Any) -> Dispatcher:
    """create_dispatcher создаёт экземпляр aiogram.Dispatcher.

    Функция используется для создания диспатчера,
    который в дальнейшем будет использован для запуска telegram бота.

    Returns:
        Dispatcher: Настроенный экземпляр диспатчера.
    """
    telegram_dispatcher: Dispatcher = Dispatcher(**kwargs)

    return telegram_dispatcher


# ----------------------------------------------------------------------------
async def configure_bot(
    bot_token: str,
    default_param: DefaultBotProperties = DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
) -> Bot:
    """configure_bot создаёт экземпляр aiogram.Bot.

    Функция используется для настройки и создания экземпляра telegram бота,
    который в дальнейшем будет передан диспатчеру для запуска.

    *Если токен бота будет не авторизован в telegram, функция не возбудит исключение.

    Args:
        bot_token (str): Токен бота.
        default_param (DefaultBotProperties, optional): Ключевые параметры для инициализации бота.

    Returns:
        Bot: Настроенный экземпляр бота.
    """
    bot = Bot(token=bot_token, default=default_param)

    return bot


# ----------------------------------------------------------------------------
async def run_bot(bot: Bot, dispatcher: Dispatcher) -> None:
    """run_bot запускает telegram бота в онлайн.

    Функция используется для инициирования запуска telegram бота,
    используя диспатчер и экземпляр бота.

    Args:
        bot (Bot): Настроенный экземпляр aiogram.Bot.
        dispatcher (Dispatcher): Настроенный экземпляр aiogram.Dispatcher.
    """
    await dispatcher.start_polling(bot)  # type: ignore
