"""Загрузка настроек бота из переменных окружения."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    """Конфигурация запуска Telegram-бота."""

    bot_token: str


def load_settings() -> Settings:
    """Считывает токен из .env и валидирует его наличие."""
    # Загружаем переменные среды из локального .env файла.
    load_dotenv()
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "Не найден BOT_TOKEN. Создайте файл .env в корне Laba11 и укажите BOT_TOKEN=..."
        )
    return Settings(bot_token=token)
