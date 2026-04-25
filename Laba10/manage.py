#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Выбираем настройки проекта перед вызовом CLI Django.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laba10site.settings')
    try:
        # Django использует этот импорт для runserver, migrate и других команд.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
