#!/usr/bin/env python
"""Точка входа Django-проекта.

Этот файл запускает административные команды Django: migrate, runserver,
создание суперпользователя и прочие служебные операции.

Журнал изменений:
- DEV-AI01 | 2026-04-11 | Причина: расширение комментариев и явная обработка ошибок импорта.
- Исходный фрагмент: прямой импорт execute_from_command_line без защитного блока try/except.
"""

import os
import sys


# Основная функция запускает внутренний механизм управления Django.
def main() -> None:
    """Выполняет старт командной строки Django.

    Исключения:
        ImportError: если Django недоступен в текущем Python-окружении.
    """

    # Указываем Django, какой файл настроек использовать.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab6site.settings")

    # Передаем управление стандартному обработчику команд Django.
    try:
        # Импортируем стандартный обработчик команд Django.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Формируем понятную причину ошибки, если Django не установлен.
        raise ImportError(
            "Не удалось импортировать Django. Проверьте активность виртуального окружения и установку зависимостей."
        ) from exc

    # Выполняем команду, переданную через терминал.
    execute_from_command_line(sys.argv)


# Этот блок позволяет запускать файл напрямую как скрипт.
if __name__ == "__main__":
    main()
