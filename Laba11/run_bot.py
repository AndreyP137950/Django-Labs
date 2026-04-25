"""Точка входа для запуска Telegram-бота лабораторной работы №11."""

from telegram_case_bot.bot import run_bot
from telegram_case_bot.config import load_settings


if __name__ == "__main__":
    # Загружаем токен и запускаем Telegram-бота.
    settings = load_settings()
    run_bot(settings.bot_token)
