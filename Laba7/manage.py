#!/usr/bin/env python
"""
Django управления проектом утилита
Позволяет запускать различные команды Django для управления проектом
"""

import os
import sys

def main():
    """Точка входа для команд управления Django"""
    # Сообщаем Django, какой модуль настроек использовать.
    # Устанавливаем переменную окружения для настроек Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Laba7.settings')
    try:
        # Подключаем исполнитель команд Django.
        # Импортируем execute_from_command_line для запуска команд
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Невозможно импортировать Django. Убедитесь, что Django установлен в вашей окружении."
        ) from exc
    
    # Выполняем команду, переданную в аргументах командной строки
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
