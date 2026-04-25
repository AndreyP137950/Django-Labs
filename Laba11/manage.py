#!/usr/bin/env python
"""
Утилита для управления Django проектом Case системы
Использование: python manage.py [command] [arguments]
"""

import os
import sys

def main():
    """Запуск команд управления Django проектом"""
    # Подключаем конфигурацию проекта case_designer.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_designer.settings')
    try:
        # Стандартный исполнитель административных команд Django.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что Django установлен "
            "и доступен в вашем окружении."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
