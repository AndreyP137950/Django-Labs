"""Небольшое in-memory хранилище состояния пользователя.

Для лабораторной работы этого достаточно: храним выбор функций отдельно для каждого user_id.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class UserConfig:
    """Конфигурация цепочки функций пользователя."""

    f1: str = "sqrt"
    f2: str = "reciprocal"
    f3: str = "exp"


class UserConfigStore:
    """Словарь user_id -> конфигурация функций."""

    def __init__(self) -> None:
        self._data: dict[int, UserConfig] = {}

    def get(self, user_id: int) -> UserConfig:
        """Возвращает конфигурацию пользователя, создавая по умолчанию при отсутствии."""
        if user_id not in self._data:
            self._data[user_id] = UserConfig()
        return self._data[user_id]
