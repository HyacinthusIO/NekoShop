# -*- coding: utf-8 -*-

"""
Описание модуля

Copyright 2024 HyacinthusIO
Лицензия Apache, версия 2.0 (Apache-2.0 license)
"""

from typing import Any


__all__: list[str] = ["on_start_bot", "on_stop_bot", "_current_state"]

__author__ = "HyacinthusIO"
__version__ = "0.6.0"


# ____________________________________________________________________________
class BotState:
    def __init__(self) -> None:
        self.__state: bool = False

    # -------------------------------------------------------------------------
    @property
    def state(self) -> bool:
        return self.__state

    # -------------------------------------------------------------------------
    @state.setter
    def state(self, new_state: bool) -> None:
        if type(new_state) is bool:
            self.__state = new_state

    # -------------------------------------------------------------------------
    def switch_state(self) -> None:
        self.state = False if self.state else True

    # -------------------------------------------------------------------------
    def __call__(self) -> Any:
        return self.state


_current_state = BotState()


# ----------------------------------------------------------------------------
async def on_start_bot() -> None:
    _current_state.switch_state()


# ----------------------------------------------------------------------------
async def on_stop_bot() -> None:
    _current_state.switch_state()
