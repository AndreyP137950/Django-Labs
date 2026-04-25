#!/usr/bin/env python
"""Точка входа Django-проекта Laba8.

Файл запускает стандартные команды Django: runserver, makemigrations,
migrate, createsuperuser и другие.
"""

import os
import sys


# Настраиваем модуль конфигурации Django до импорта management-команд.
def main() -> None:
    """Запускает утилиты командной строки Django."""
    # Подключаем модуль настроек проекта до запуска command-line утилиты.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lab8site.settings")
    # Стандартный исполнитель команд Django.
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
