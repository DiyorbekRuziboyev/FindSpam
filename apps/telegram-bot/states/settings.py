from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class GroupSettingsForm(StatesGroup):
    select_language = State()
    set_spam_threshold = State()
    set_flood_threshold = State()
    confirm_settings = State()
