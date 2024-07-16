# -*- coding: utf-8 -*-

__all__: list[str] = ["bot_send_message_to_chat"]

import aiohttp


async def bot_send_message_to_chat(
    bot_token: str, chat_id: str, message_text: str
) -> None:
    async with aiohttp.ClientSession() as session:
        await session.post(
            url=f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": message_text},
        )
